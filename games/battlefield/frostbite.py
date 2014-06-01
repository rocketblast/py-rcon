# -*- coding: utf-8 -*-
# These functions are taken from the official BC2 documentation by DICE

from struct import *
import socket
import sys
import shlex
import string
import os
import hashlib

###################################################################################

# Packet encoding/decoding helper functions

def EncodeHeader(isFromServer, isResponse, sequence):
    header = sequence & 0x3fffffff
    if isFromServer:
        header += 0x80000000
    if isResponse:
        header += 0x40000000
    return pack('<I', header)

def DecodeHeader(data):
    [header] = unpack('<I', data[0 : 4])
    return [header & 0x80000000, header & 0x40000000, header & 0x3fffffff]

def EncodeInt32(size):
    return pack('<I', size)

def DecodeInt32(data):
    return unpack('<I', data[0 : 4])[0]


def EncodeWords(words):
    size = 0
    encodedWords = ''
    for word in words:
        strWord = str(word)
        encodedWords += EncodeInt32(len(strWord))
        encodedWords += strWord
        encodedWords += '\x00'
        size += len(strWord) + 5
    return size, encodedWords

def DecodeWords(size, data):
    numWords = DecodeInt32(data[0:])
    words = []
    offset = 0
    while offset < size:
        wordLen = DecodeInt32(data[offset : offset + 4])
        word = data[offset + 4 : offset + 4 + wordLen]
        words.append(word)
        offset += wordLen + 5
    return words

def EncodePacket(isFromServer, isResponse, sequence, words):
    encodedHeader = EncodeHeader(isFromServer, isResponse, sequence)
    encodedNumWords = EncodeInt32(len(words))
    [wordsSize, encodedWords] = EncodeWords(words)
    encodedSize = EncodeInt32(wordsSize + 12)
    return encodedHeader + encodedSize + encodedNumWords + encodedWords

# Decode a request or response packet
# Return format is:
# [isFromServer, isResponse, sequence, words]
# where
#	isFromServer = the command in this command/response packet pair originated on the server
#   isResponse = True if this is a response, False otherwise
#   sequence = sequence number
#   words = list of words

def DecodePacket(data):
    [isFromServer, isResponse, sequence] = DecodeHeader(data)
    wordsSize = DecodeInt32(data[4:8]) - 12
    words = DecodeWords(wordsSize, data[12:])
    return [isFromServer, isResponse, sequence, words]

###############################################################################

clientSequenceNr = 0

# Encode a request packet

def EncodeClientRequest(words):
    global clientSequenceNr
    packet = EncodePacket(False, False, clientSequenceNr, words)
    clientSequenceNr = (clientSequenceNr + 1) & 0x3fffffff
    return packet

# Encode a response packet

def EncodeClientResponse(sequence, words):
    return EncodePacket(True, True, sequence, words)

###################################################################################

def generatePasswordHash(salt, password):
    m = hashlib.md5()
    m.update(salt)
    m.update(password)
    return m.digest()

###################################################################################

def containsCompletePacket(data):
    if len(data) < 8:
        return False
    if len(data) < DecodeInt32(data[4:8]):
        return False
    return True

# Wait until the local receive buffer contains a full packet (appending data from the network socket),
# then split receive buffer into first packet and remaining buffer data

def receive_packet(socket, receiveBuffer):

    while not containsCompletePacket(receiveBuffer):
        receiveBuffer += socket.recv(4096)

    packetSize = DecodeInt32(receiveBuffer[4:8])

    packet = receiveBuffer[0:packetSize]
    receiveBuffer = receiveBuffer[packetSize:len(receiveBuffer)]

    return [packet, receiveBuffer]

###################################################################################

def send_packet(socket, data):

    receiveBuffer = ""

    getRequest = EncodeClientRequest( data )
    socket.send(getRequest)

    [getResponse, receiveBuffer] = receive_packet(socket, receiveBuffer)
    [isFromServer, isResponse, sequence, words] = DecodePacket(getResponse)

    return words

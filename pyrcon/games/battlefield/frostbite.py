# -*- coding: utf-8 -*-
# These functions are taken from the official BC2 documentation by DICE and then modified to fit our needs

import hashlib
import os
import sys
import shlex
import string

from struct import *

class Frostbite:
    clientSequenceNr = 0

    @staticmethod
    def EncodeHeader(isFromServer, isResponse, sequence):
        header = sequence & 0x3fffffff
        if isFromServer:
            header += 0x80000000
        if isResponse:
            header += 0x40000000
        return pack('<I', header) 

    @staticmethod
    def DecodeHeader(data):
    	[header] = unpack('<I', data[0 : 4])
    	return [header & 0x80000000, header & 0x40000000, header & 0x3fffffff]

    @staticmethod
    def EncodeInt32(size):
    	return pack('<I', size)

    @staticmethod
    def DecodeInt32(data):
        return unpack('<I', data[0 : 4])[0]

    @staticmethod
    def EncodeWords(words):
        size = 0
        encodedWords = ''
        for word in words:
            strWord = str(word)
            encodedWords += Frostbite.EncodeInt32(len(strWord))
            encodedWords += strWord
            encodedWords += '\x00'
            size += len(strWord) + 5
        return size, encodedWords

    @staticmethod
    def DecodeWords(size, data):
        numWords = Frostbite.DecodeInt32(data[0:])
        words = []
        offset = 0
        while offset < size:
            wordLen = Frostbite.DecodeInt32(data[offset : offset + 4])
            word = data[offset + 4 : offset + 4 + wordLen]
            words.append(word)
            offset += wordLen + 5
        return words

    @staticmethod
    def EncodePacket(isFromServer, isResponse, sequence, words):
        encodedHeader = Frostbite.EncodeHeader(isFromServer, isResponse, sequence)
        encodedNumWords = Frostbite.EncodeInt32(len(words))
        [wordsSize, encodedWords] = Frostbite.EncodeWords(words)
        encodedSize = Frostbite.EncodeInt32(wordsSize + 12)
        return encodedHeader + encodedSize + encodedNumWords + encodedWords

    @staticmethod
    def DecodePacket(data):
        [isFromServer, isResponse, sequence] = Frostbite.DecodeHeader(data)
        wordsSize = Frostbite.DecodeInt32(data[4:8]) - 12
        words = Frostbite.DecodeWords(wordsSize, data[12:])
        return [isFromServer, isResponse, sequence, words]

    @staticmethod
    def EncodeClientRequest(words):
        #Frostbite.clientSequenceNr
        packet = Frostbite.EncodePacket(False, False, Frostbite.clientSequenceNr, words)
        Frostbite.clientSequenceNr = (Frostbite.clientSequenceNr + 1) & 0x3fffffff
        return packet

    # Encode a response packet
    @staticmethod
    def EncodeClientResponse(sequence, words):
        return Frostbite.EncodePacket(True, True, sequence, words)

    @staticmethod
    def generatePasswordHash(salt, password):
        m = hashlib.md5()
        m.update(salt)
        m.update(password)
        return m.digest()

    @staticmethod
    def containsCompletePacket(data):
        if len(data) < 8:
            return False
        if len(data) < Frostbite.DecodeInt32(data[4:8]):
            return False
        return True
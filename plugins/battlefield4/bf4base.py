# -*- coding: utf-8 -*-

# File: base.py
# Description: Base class for battlefield plugins

import abc

class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def on_connect(self, data):
        ''' player.onConnect '''
        return

    @abc.abstractmethod
    def on_authenticated(self, data):
        ''' player.onAuthenticated '''
        return

    @abc.abstractmethod
    def on_join(self, data):
        ''' player.onJoin '''
        return

    @abc.abstractmethod
    def on_leave(self, data):
        ''' player.onLeave '''
        return

    @abc.abstractmethod
    def on_spawn(self, data):
        ''' player.onSpawn '''
        return

    @abc.abstractmethod
    def on_kill(self, data):
        ''' player.onKill '''
        return

    @abc.abstractmethod
    def on_chat(self, data):
        ''' player.onChat '''
        return

    @abc.abstractmethod
    def on_squadchange(self, data):
        ''' player.onSquadChange '''
        return

    @abc.abstractmethod
    def on_teamchange(self, data):
        ''' player.onTeamChange '''
        return

    @abc.abstractmethod
    def on_pb(self, data):
        ''' punkbuster.onMessage '''
        return

    @abc.abstractmethod
    def on_maxplayerchange(self, data):
        ''' server.onMaxPlayerCountChange '''
        return

    @abc.abstractmethod
    def on_levelload(self, data):
        ''' server.onLevelLoaded '''
        return

    @abc.abstractmethod
    def on_roundover(self, data):
        ''' server.onRoundOver '''
        return

    @abc.abstractmethod
    def on_roundoverscore(self, data):
        ''' server.onRoundOverTeamScores '''
        return

    @abc.abstractmethod
    def on_roundoverplayers(self, data):
        ''' server.onRoundOverPlayers '''
        return

    @abc.abstractmethod
    def on_unknown(self, data):
        ''' unknwon event '''
        return

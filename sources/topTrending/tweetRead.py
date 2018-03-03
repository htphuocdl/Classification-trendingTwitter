#http://www.awesomestats.in/spark-twitter-stream/
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key = 'WNCJqVbE2yxgVPRFcEnbPI5o8'
consumer_secret = 'kHwiX4g8AwNgBdhFSNCFTToV641JThrHABeH3ygHdZjGO2TYd0'
access_token = '775716170867453952-PIvMRyO5Fa5zbHCKleCNKQ6ec2hG3uX'
access_secret = 'vNy7xHngpD3pb3BSxnw8RjZKjcVzLucLLZYrfNDfE8dQH'

class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
      try:
          msg = json.loads( data )
          print( msg['text'].encode('utf-8') )
          self.client_socket.send( msg['text'].encode('utf-8') )
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track=['trump'])

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "172.16.125.105"      # Get local machine name
  port = 5555                 # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )

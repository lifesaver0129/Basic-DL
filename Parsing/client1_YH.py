#-*- coding: UTF-8 -*-


from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
import base64, json

# 继承WebSocketServerProtocol类  
class MyClientProtocol(WebSocketClientProtocol):
    # 建立websocket时调用的函数
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            # opening the image file and encoding in base64
            with open("2.jpg", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            encoded = {'IMG':encoded_string}
            encode_string = json.dumps(encoded)
            # printing the size of the encoded image which is sent

            # sending the encoded image
            self.sendMessage(encode_string.encode('utf8'))
            print("Encoded size of the sent image: {0} bytes".format(len(encode_string)))
        hello()

    # 收到消息后的处理函数，其中binary指示是字符串形式还是二进制
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
            msg = json.loads(payload)
            img = msg['seg1'] 
            #print msg['FeaPts']      
            #msg = json.loads(payload)
            # decode the image and save locally

            with open("image_received2.png", "wb") as image_file:
                image_file.write(base64.b64decode(img))
        else:
            # printing the size of the encoded image which is received         
            msg = json.loads(payload)
            img = msg['seg1']          
            #print msg['FeaPts']              
            
            #msg = json.loads(payload)         
            # decode the image and save locally                     
            with open("image_received2.png", "wb") as image_file:            
                image_file.write(base64.b64decode(img))         
            print("Encoded size of the received image: {0} bytes".format(len(payload)))

    # websocket关闭时调用的函数，其中wasClean指示是否正常关闭，code指示关闭状态，reason指示原因
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':
    import sys
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)
    factory = WebSocketClientFactory("ws://158.132.122.72:9000")
    factory.protocol = MyClientProtocol
    reactor.connectTCP("158.132.122.72", 9000, factory)#@UndefinedVariable

    reactor.run()#@UndefinedVariable
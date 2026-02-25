# 단순한 HTTPServer 구축 - 기본적인 socket 연결 관ㄹ리

from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 7777

handler = SimpleHTTPRequestHandler # 문서를 읽어 클라이언트로 전송하는 역할

# HTTPServer 객체 생성
serv = HTTPServer(('192.168.0.39',PORT),handler)
print('웹 서비스 시작...')

serv.serve_forever()   # 웹서비스 무한 루핑




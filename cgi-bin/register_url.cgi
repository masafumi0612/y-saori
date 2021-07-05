#!/usr/bin/ruby

#rubyのexeファイルを実行時に指定すること

#puts "Content-type: text/html\n\n"; #\n\nを加えないとエラーになってしまう(ログを見て確認)

require 'cgi'
require_relative '../lib/source_url_controller'

def html_head
    return <<~EOF_HTML
    Content-Type: text/html
  
    <html>
    <head>
    <title>文書管理情報取得元入力</title>
    <meta http-equiv="content-type" charset="utf-8">
    </head>
    <center>
    <body>
    <font size=6>文書管理情報取得元入力</font>
    EOF_HTML
end

def html_message(msg)
  return <<~EOF_HTML
    <h3>#{msg}</h3>
  EOF_HTML
end

def html_body(url,register)
    return <<~EOF_HTML
      <div>#{url},#{register}</div>

      <form action="register_url.cgi" method="POST" class="form-example">
        <div class="form-example">
          <label for="name">url: </label>
          <input type="text" name="url" id="name" required>
        </div>
        <div class="form-example">
          <label for="name">register : </label>
          <input type="text" name="register" id="name">
        </div>
          <div class="form-example">
          <input type="submit" value="Subscribe!">
        </div>
      </form>
    </body>
    </center>
    EOF_HTML
end

def html_foot
    return <<~EOF_HTML
    <center>
    <a href="../html/index.html">TOPへ戻る</a>
    <center>
    </body>
    </html>
    EOF_HTML
end

content = []

input = CGI.new
url = input["url"].to_s
register = input["register"].to_s

# ここにSourceURLControllerのadd処理
# srcURLcon = SourceURLController.new
# err_value = srcURLcon.add(url, register)
# 返り値は登録できたかどうかのエラー値（bool値）

if url != ""
  cont = SourceURLController.new
  cont.add(url, register)
end

err_value = 0 # 仮のエラー値

content << html_head

if (err_value==0) then
  msg="登録完了"
elsif (err_value==1) then
  msg="エラー"
else
  mag=""
end

content << html_message(msg)
content << html_body(url, register)
content << html_foot

puts content

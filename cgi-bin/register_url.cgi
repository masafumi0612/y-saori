#!/usr/bin/ruby

#rubyのexeファイルを実行時に指定すること

#puts "Content-type: text/html\n\n"; #\n\nを加えないとエラーになってしまう(ログを見て確認)

require 'cgi'
require_relative '../lib/source_url_controller'

NORMAL = 0
CONSTRAINT_ERR = 1
BLANK_ERR = 2
DUPLICATION_ERR = 3
LIMIT_ERR = 4

URL_LEN = 2048
REGISTER_NAME_LEN = 128

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

def html_message(err_value)
  case err_value
  when NORMAL then
    msg="※文書管理情報取得元の登録が完了しました．"
  when CONSTRAINT_ERR then 
    msg="※URLには半角記号\-\_\.\!\'\(\)\;\/\?\:\@\&\=\+\$\,\%\#と半角英数字のみ入力できます
        <br>URLの最大文字数は2048文字です．
        <br>登録名の最大文字数は128文字です．"
  when BLANK_ERR then 
    msg="※URLが入力されていません．"
  when DUPLICATION_ERR then
    msg="※すでに追加されたURLです．" 
  when LIMIT_ERR then
    msg="※すでに10個の文書管理情報が登録されています．10より少なくなるように削除してください．" 
  else
    msg=""
  end

  return <<~EOF_HTML
    <h3>#{msg}</h3>
  EOF_HTML
end

def html_body
    return <<~EOF_HTML
      <form action="register_url.cgi" method="POST" class="form-example">    
        <table border=1 bgcolor =#FFFFFF>
          <tr>
            <td bgcolor =#CCFFFF>
              URL
            </td>
            <td>
              <input type="text" name="url" id="name">
            </td>
          </tr>
          <tr>
            <td bgcolor =#CCFFFF>
              登録名
            </td>
            <td>
              <input type="text" name="register_name" id="name">
            </td>
          </tr>
        </table><br>
        
        <input type="submit" value="追加">
        <input name="submit_flag" type="hidden" value="on">
        </form>
    EOF_HTML
end

def html_foot
    return <<~EOF_HTML
    <a href="../html/index.html">TOPへ戻る</a>
    </center>
    </body>
    </html>
    EOF_HTML
end

def html_test(test)
  return <<~EOF_HTML
    <h3>表示テスト：#{test}</h3>
  EOF_HTML
end

content = []

input = CGI.new
url = input["url"].to_s
register_name = input["register_name"].to_s

if /[^\w\-\_\.\!\'\(\)\;\/\?\:\@\&\=\+\$\,\%\#]/ =~ url || url.length > URL_LEN || register_name.length > REGISTER_NAME_LEN
  err_value = CONSTRAINT_ERR
elsif input["submit_flag"]=="on" && url == ""
  err_value = BLANK_ERR
elsif input["submit_flag"]=="on"
  url = CGI.escapeHTML(url) 
  register_name = CGI.escapeHTML(register_name)
  cont = SourceURLController.new
  err_value = cont.add(url, register_name)
end 

content << html_head
content << html_message(err_value)
content << html_body
content << html_foot

puts content

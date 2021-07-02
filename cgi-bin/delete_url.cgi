#!/usr/bin/ruby

#rubyのexeファイルを実行時に指定すること

#puts "Content-type: text/html\n\n"; #\n\nを加えないとエラーになってしまう(ログを見て確認)

require 'cgi'
require 'json'
require '../lib/source_url_controller.rb'

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
  if (err_value==0) then
    msg="削除完了"
  elsif (err_value==1) then
    msg="エラー"
  else
    mag=""
  end
  
  return <<~EOF_HTML
    <h3>#{msg}</h3>
    <form action="delete_url.cgi" method="POST" class="form-example">
  EOF_HTML
end

def html_checkbox(url, register_name)
  return <<~EOF_HTML
      <div>
        <div class="form-example"><input type="text" id="name" value="#{url}"></div>
        <div class="form-example"><input type="text" id="name" value="#{register_name}"></div>
        <input type="checkbox" name="#{url}" id="name" value="#{url},#{register_name}">
      </div>
  EOF_HTML
end

def html_body
    return <<~EOF_HTML
        <input type="submit" value="削除">
      </form>
    EOF_HTML
end

def html_test(test)
  return <<~EOF_HTML
    <h3>#{test}</h3>
  EOF_HTML
end

def html_foot
    return <<~EOF_HTML
    <a href="../html/index.html">TOPへ戻る</a>
    </body>
    </center>
    </html>
    EOF_HTML
end

#####_main_#####

hash = File.open("../database/register.json") do |j|
  JSON.load(j)
end

input = CGI.new

# for i in input.keys do 
#   input[i]を分割
#   SorceURLController.delete(input[i][1],input[i][2])
# end

err_value = 1 # 仮のエラー値

content = []
content << html_head
content << html_message(err_value)

for register_info in hash do
  content << html_checkbox(register_info["url"],register_info["register_name"])
end

content << html_body

# チェックの入ったurl,登録名のみ保存できているか確認用
for key in input.keys do # keyはurl
  content << html_test(input[key]) 
end

content << html_foot

puts content

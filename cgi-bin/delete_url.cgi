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
    <font size=6>文書管理情報取得元削除</font>
    EOF_HTML
end

def html_message(err_value, msg_value)
  if (err_value==0) then
    err_msg="※ 削除完了"
  elsif (err_value==1) then
    err_msg="※ エラー"
  else
    err_mag=""
  end

  if (msg_value==true) then
    msg="削除したい項目を選択してください"
  else
    msg="URLが登録されていません"
  end
  
  return <<~EOF_HTML
    <h3>#{err_msg}</h3>
    <h3>※ #{msg}</h3>
    EOF_HTML
end

def html_body
  return <<~EOF_HTML
  <form action="delete_url.cgi" method="POST" class="form-example">
  <table border=1 bgcolor =#FFFFFF>
      <tr>
        <td bgcolor =#CCFFFF rowspan="2" width="25" align="center">No</td>
        <td>
          <input type="text" value="URL" readonly>
        </td>
        <td rowspan="2" width="25"></td>
      </tr>
      <tr>
        <td>
          <input type="text" value="登録名" readonly>
        </td>
      </tr>
    </table><br>
  EOF_HTML
end 

def html_checkbox(url, register_name,i)
  return <<~EOF_HTML
    <table border=1 bgcolor =#FFFFFF>
      <tr>
        <td bgcolor =#CCFFFF rowspan="2" width="25" align="center">#{i}</td>
        <td>
          <input type="text" id="name" value="#{url}" readonly>
        </td>
        <td rowspan="2" width="25" align="center">
          <input type="checkbox" name="#{url}" id="name" value="#{url},#{register_name}">
        </td>
      </tr>
      <tr>
        <td>
          <input type="text" id="name" value="#{register_name}" readonly>
        </td>
      </tr>
    </table>
  EOF_HTML
end

def html_foot
    return <<~EOF_HTML
    <input type="submit" value="削除">
    </form>
    <a href="../html/index.html">TOPへ戻る</a>
    </body>
    </center>
    </html>
    EOF_HTML
end

def html_test(test)
  return <<~EOF_HTML
    <h3>表示テスト：#{test}</h3>
  EOF_HTML
end

#####_main_#####
input = CGI.new
cont = SourceURLController.new

for key in input.keys do # keyはPOSTされたURL
   url, register_name = input[key].split(",")
   cont.delete(url, register_name)
end

msg_value = cont.list.any?
err_value = "" # 仮のエラー値

content = []
content << html_head
content << html_message(err_value, msg_value)
content << html_body

cont.list.each.with_index(1) do |register_info, i|
  content << html_checkbox(register_info["url"],register_info["register_name"],i)
end

content << html_test(url) 
content << html_test(register_name) 

# チェックの入ったurl,登録名のみ保存できているか確認用
# for key in input.keys do # keyはurl
#   content << html_test(input[key]) 
# end

content << html_foot

puts content

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
    err_msg="※　削除完了"
  elsif (err_value==1) then
    err_msg="※　選択されていません"
  else
    err_msg=""
  end

  if (msg_value==true) then
    msg="※　削除したい項目を選択してください"
  else
    msg="※　URLが登録されていません"
  end
  
  return <<~EOF_HTML
    <h3>#{err_msg}</h3>
    <h3>#{msg}</h3>
    EOF_HTML
end

def html_body
  return <<~EOF_HTML
  <form action="delete_url.cgi" method="POST" class="form-example" onSubmit="return check()">
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
          <input type="text" name="#{i}" value="#{url}" readonly>
        </td>
        <td rowspan="2" width="25" align="center">
          <input type="checkbox" name="No" value="#{i}">
        </td>
      </tr>
      <tr>
        <td>
          <input type="text" name="#{i}" value="#{register_name}" readonly>
        </td>
      </tr>
    </table>
  EOF_HTML
end

def html_foot
    return <<~EOF_HTML
    <input type="submit" value="削除">
    <input name="submit_flag" type="hidden" value="on">
    </form>
    <a href="../html/index.html">TOPへ戻る</a>
    <script>
    function check(){
      if(window.confirm('削除しますか？')){
        return true;
      }else{
        return false;
      }
    }
    </script>
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
params = input.params

for del_num in params["No"]
  url,register_name = params[del_num]
  cont.delete(url, register_name)
end

msg_value = cont.list.any? # 取得元が登録されているか

if(params=={}) then 
  err_value = 2
elsif((params["submit_flag"]==["on"]) && (params["No"]==[])) then # チェックボックスにチェックが入ってない
  err_value = 1
else
  err_value = 0
end

content = []
content << html_head
content << html_message(err_value, msg_value)
content << html_body

cont.list.each.with_index(1) do |register_info, i|
  content << html_checkbox(register_info["url"],register_info["register_name"],i)
end

# チェックの入ったurl,登録名のみ保存できているか確認用
# for x in params["No"] do # keyはurl
#   content << html_test(params[x]) 
# end

content << html_foot

puts content

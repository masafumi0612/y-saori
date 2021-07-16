#!/usr/bin/ruby

#rubyのexeファイルを実行時に指定すること

#puts "Content-type: text/html\n\n"; #\n\nを加えないとエラーになってしまう(ログを見て確認)

require 'cgi'
require 'json'
require '../lib/source_url_controller.rb'

NORMAL = 0
NO_SELECT_ERR = 1

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
  case err_value
  when NORMAL then
    err_msg="※選択した項目の削除が完了しました．"
  when NO_SELECT_ERR then
    err_msg="※削除する項目が選択されていません．"
  else
    err_msg=""
  end

  case msg_value
  when true then
    msg="※削除する項目を選択してください．"
  when false then
    msg="※文書管理情報取得元が登録されていません．"
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
          <input type="checkbox" name="info_num" value="#{i}">
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
    <br>
    <input type="submit" value="削除">
    <input name="submit_flag" type="hidden" value="on">
    </form>
    <a href="../html/index.html">TOPへ戻る</a>
    <script>
    function check(){
      if(window.confirm('選択した項目を削除しますか？')){
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
params = input.params

cont = SourceURLController.new

for del_num in params["info_num"]
  url,register_name = params[del_num]
  cont.delete(url, register_name)
end

register_info_list = cont.list

msg_value = register_info_list.any? # 取得元が登録されているか

if((params["submit_flag"]==["on"]) && (params["info_num"]==[])) then # チェックボックスにチェックが入ってない
  err_value = NO_SELECT_ERR
elsif((params["submit_flag"]==["on"]) && (!(params["info_num"]==[]))) then # チェックボックスにチェックが入ってない 
  err_value = NORMAL
end

content = []
content << html_head
content << html_message(err_value, msg_value)
content << html_body

register_info_list.each.with_index(1) do |register_info, i|
  content << html_checkbox(register_info["url"],register_info["register_name"],i)
end

content << html_foot

puts content

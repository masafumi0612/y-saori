#!/usr/bin/ruby

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
    <link rel="stylesheet" href="../style.css">
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
        <td bgcolor =#CCFFFF rowspan="2" width="40" align="center">No</td>
        <td class="register_text">
          <input type="text" class="register_text" value="URL" readonly>
        </td>
        <td rowspan="2" width="40"></td>
      </tr>
      <tr>
        <td class="register_text">
          <input type="text" class="register_text" value="登録名" readonly>
        </td>
      </tr>
    </table><br>
  EOF_HTML
end 

def html_checkbox(url, register_name,i)
  return <<~EOF_HTML
    <table border=1 bgcolor =#FFFFFF>
      <tr>
        <td bgcolor =#CCFFFF rowspan="2" class="del_index" align="center">#{i}</td>
        <td class="register_text">
          <input type="text" name="#{i}" value="#{url}" class="register_text" readonly>
        </td>
        <td rowspan="2" class="del_index" align="center">
          <input type="checkbox" name="info_num" value="#{i}" style="transform:scale(1.2);">
        </td>
      </tr>
      <tr>
        <td class="register_text">
          <input type="text" name="#{i}" value="#{register_name}" class="register_text" readonly>
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
    <a href="../index.html">TOPへ戻る</a>
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
  url = CGI.escapeHTML(url)
  register_name = CGI.escapeHTML(register_name)
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

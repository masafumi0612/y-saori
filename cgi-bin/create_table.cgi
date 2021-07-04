#!/usr/bin/ruby

require 'cgi'
require 'cgi/session'
require_relative '../lib/source_url_controller'
require_relative '../lib/document_info_controller'
require_relative '../lib/document_info'

def html_head
  return <<~EOF_HTML
  Content-Type: text/html

  <html>
  <head>
  <title>文書管理統計表の閲覧・ダウンロード</title>
  <meta http-equiv="content-type" charset="utf-8">
  <script src="http://code.jquery.com/jquery-latest.min.js"></script>
  </head>
  <body>
  <center>
  <form action="create_table.cgi" method="POST" enctype="multipart/form-data"　style="float:left">
  <font size=6>文書管理統計表の閲覧・ダウンロード</font>
    <h3>メッセージ欄</h3>
  EOF_HTML
end

def html_message(msg)
  return <<~EOF_HTML
  <p>#{msg}</p>
  EOF_HTML
end

def html_url_table(url_list, send_url)
  pulldown_list = url_pulldown(url_list)
  return <<~EOF_HTML
  <p><font color=#CC0000>※登録済みのURLから一つ選択してください</font></p>
  <table border=1 bgcolor =#FFFFFF>
  <tr>
    <td bgcolor =#CCFFFF>
      URL
    </td>
    <td>
      <select name="send_url">
        #{pulldown_list}
      </select>
    </td>
  </tr>
  </table>
  EOF_HTML
end

def url_pulldown(url_list)
  pulldown_list = ""
  pulldown_list << "<option value = "">""</option>\n"
  i = 2
  for url_and_name in url_list
    content = "#{url_and_name["register_name"]}(#{url_and_name["url"]})"
    pulldown = "<option value = #{url_and_name["url"]}>#{content}</option>\n"
    pulldown_list << pulldown
    i = i + 1
  end
  return pulldown_list
end

def html_select_year(from_year_form0, to_year_form0, form0,
                      from_year_form1, to_year_form1, form1,
                      from_year_form2, to_year_form2, form2,
                      from_year_form3, to_year_form3, form3,
                      from_year_form4, to_year_form4, form4,
                      from_year_form5, to_year_form5, form5,
                      from_year_form6, to_year_form6, form6,
                      from_year_form7, to_year_form7, form7,
                      from_year_form8, to_year_form8, form8,
                      from_year_form9, to_year_form9, form9)
forms = [form0, form1, form2, form3, form4, form5, form6, form7, form8, form9]
to_year_forms = [to_year_form0, to_year_form1, to_year_form2, to_year_form3, to_year_form4, to_year_form5, to_year_form6, to_year_form7, to_year_form8, to_year_form9]
forms_type = ["hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden"]
from_year_forms_type = ["hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden"]
to_year_forms_type = ["hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden"]
waves = ["", "", "", "", "", "", "", "", "", ""]

for i in 0..forms.length
  if forms[i] != ""
    forms_type[i] = "checkbox"
    from_year_forms_type[i] = "text"
    if to_year_forms[i] != ""
      to_year_forms_type[i] = "text"
      waves[i] = "~"
    end
  end
end

  return <<~EOF_HTML
  <table border="1">
  <tr>
  <td>年度</td>
  <td>1つ追加</td>
  <td><button type="button" id="single_year_form">+</button></td>
  <td>まとめて追加</td>
  <td><button type="button" id="multiple_year_form">+</button></td>
  </tr>
  </table>
  <table>
  <tr>
  <td><input type="#{forms_type[0]}" name="form0" id="form0" value="#{form0}"></td>
  <td><input type="#{from_year_forms_type[0]}" name="from_year_form0" id="from_year_form0" value="#{from_year_form0}"></td>
  <td><div id="form0_wave">#{waves[0]}</div></td>
  <td><input type="#{to_year_forms_type[0]}" name="to_year_form0" id="to_year_form0" value=#{to_year_form0}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[1]}" name="form1" id="form1" value='#{form1}'></td>
  <td><input type="#{from_year_forms_type[1]}" name="from_year_form1" id="from_year_form1" value="#{from_year_form1}"></td>
  <td><div id="form1_wave">#{waves[1]}</div></td>
  <td><input type="#{to_year_forms_type[1]}" name="to_year_form1" id="to_year_form1" value=#{to_year_form1}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[2]}" name="form2" id="form2" value='#{form2}'></td>
  <td><input type="#{from_year_forms_type[2]}" name="from_year_form2" id="from_year_form2" value="#{from_year_form2}"></td>
  <td><div id="form2_wave">#{waves[2]}</div></td>
  <td><input type="#{to_year_forms_type[2]}" name="to_year_form2" id="to_year_form2" value=#{to_year_form2}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[3]}" name="form3" id="form3" value='#{form3}'></td>
  <td><input type="#{from_year_forms_type[3]}" name="from_year_form3" id="from_year_form3" value="#{from_year_form3}"></td>
  <td><div id="form3_wave">#{waves[3]}</div></td>
  <td><input type="#{to_year_forms_type[3]}" name="to_year_form3" id="to_year_form3" value=#{to_year_form3}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[4]}" name="form4" id="form4" value='#{form4}'></td>
  <td><input type="#{from_year_forms_type[4]}" name="from_year_form4" id="from_year_form4" value="#{from_year_form4}"></td>
  <td><div id="form4_wave">#{waves[4]}</div></td>
  <td><input type="#{to_year_forms_type[4]}" name="to_year_form4" id="to_year_form4" value=#{to_year_form4}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[5]}" name="form5" id="form5" value='#{form5}'></td>
  <td><input type="#{from_year_forms_type[5]}" name="from_year_form5" id="from_year_form5" value="#{from_year_form5}"></td>
  <td><div id="form5_wave">#{waves[5]}</div></td>
  <td><input type="#{to_year_forms_type[5]}" name="to_year_form5" id="to_year_form5" value=#{to_year_form5}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[6]}" name="form6" id="form6" value='#{form6}'></td>
  <td><input type="#{from_year_forms_type[6]}" name="from_year_form6" id="from_year_form6" value="#{from_year_form6}"></td>
  <td><div id="form6_wave">#{waves[6]}</div></td>
  <td><input type="#{to_year_forms_type[6]}" name="to_year_form6" id="to_year_form6" value=#{to_year_form6}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[7]}" name="form7" id="form7" value='#{form7}'></td>
  <td><input type="#{from_year_forms_type[7]}" name="from_year_form7" id="from_year_form7" value="#{from_year_form7}"></td>
  <td><div id="form7_wave">#{waves[7]}</div></td>
  <td><input type="#{to_year_forms_type[7]}" name="to_year_form7" id="to_year_form7" value=#{to_year_form1}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[8]}" name="form8" id="form8" value='#{form8}'></td>
  <td><input type="#{from_year_forms_type[8]}" name="from_year_form8" id="from_year_form8" value="#{from_year_form8}"></td>
  <td><div id="form8_wave">#{waves[0]}</div></td>
  <td><input type="#{to_year_forms_type[8]}" name="to_year_form8" id="to_year_form8" value=#{to_year_form8}></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[9]}" name="form9" id="form9" value='#{form9}'></td>
  <td><input type="#{from_year_forms_type[9]}" name="from_year_form9" id="from_year_form9" value="#{from_year_form9}"></td>
  <td><div id="form9_wave">#{waves[9]}</div></td>
  <td><input type="#{to_year_forms_type[9]}" name="to_year_form9" id="to_year_form9" value=#{to_year_form9}></td>
  </tr>
  </table>
  <table border="1">
  <div id="year_form_field"></div>
  </table>
  <script>
//  window.onload = function(){
    document.getElementById("single_year_form").onclick = function(){
      for(let i = 0; i < 10; i++){
        if(document.getElementById("form"+i).value == ""){
          document.getElementById("form"+i).value = "checked";
          document.getElementById("form"+i).checked = "checked";
          document.getElementById("form"+i).type="checkbox";
          document.getElementById("from_year_form"+i).type="text";
          break;
        }
      }
    }

    document.getElementById("multiple_year_form").onclick = function(){
      for(let i = 0; i < 10; i++){
        if(document.getElementById("form"+i).value == ""){
          document.getElementById("form"+i).value = "checked";
          document.getElementById("form"+i).checked = "checked";
          document.getElementById("form"+i).type="checkbox";
          document.getElementById("from_year_form"+i).type="text";
          document.getElementById("form"+i+"_wave").innerHTML = "~";
          document.getElementById("to_year_form"+i).type="text";
          break;
        }
      }
    }

    function remove_form(){
      if (this.checked){
      }else{
        this.type = "hidden";
        this.value = "";
        document.getElementById("from_year_"+this.id).type = "hidden";
        document.getElementById("from_year_"+this.id).value = "";
        document.getElementById(this.id+"_wave").innerHTML = "";
        document.getElementById("to_year_"+this.id).type="hidden";
        document.getElementById("to_year_"+this.id).value = "";
      }
    }

    for(let i = 0; i < 10; i++)
    {
      if(document.getElementById("form"+i).value == "checked"){
        document.getElementById("form"+i).checked = "checked";
      }
    }

    var form0 = document.getElementById("form0");
    var form1 = document.getElementById("form1");
    var form2 = document.getElementById("form2");
    var form3 = document.getElementById("form3");
    var form4 = document.getElementById("form4");
    var form5 = document.getElementById("form5");
    var form6 = document.getElementById("form6");
    var form7 = document.getElementById("form7");
    var form8 = document.getElementById("form8");
    var form9 = document.getElementById("form9");

    form0.onclick = remove_form;
    form1.onclick = remove_form;
    form2.onclick = remove_form;
    form3.onclick = remove_form;
    form4.onclick = remove_form;
    form5.onclick = remove_form;
    form6.onclick = remove_form;
    form7.onclick = remove_form;
    form8.onclick = remove_form;
    form9.onclick = remove_form;

  </script>
  EOF_HTML
end

def html_select_tables_and_graph
  return <<~EOF_HTML
  <p><font color=#CC0000>※表示またはダウンロードしたい作成物を選択してください</font></p>
  <table border="1">
  <tr>
  <td rowspan="3">作成物</td>
  <td><input name="single" type="checkbox" value="1"></td>
  <td>提出回数集計表</td>
  </tr>
  <tr>
  <td><input name="multiple" type="checkbox" value="1"></td>
  <td>提出回数集計表</td>
  </tr>
  <tr>
  <td><input name="graph" type="checkbox" value="1"></td>
  <td>平均提出回数比較グラフ</td>
  </tr>
  </table>
  EOF_HTML
end

def html_print_and_download(msg)
  return <<~EOF_HTML
  <table border="0">
  <tr>
  <td><input name="commit" type="submit" value="表示"/>
  <input name="msg" type="hidden" value="#{msg}">
  </td>
  <td><input name="commit" type="submit" value="ダウンロード"/>
  <input name="msg" type="hidden" value="#{msg}">
  </td>
  </tr>
  </table>
  EOF_HTML
end

def html_result
  return <<~EOF_HTML
  <p>結果を表示</p>
  EOF_HTML
end

def html_foot
  return <<~EOF_HTML
  <a href="../html/index.html">トップへ戻る</a>
  </form>
  </center>
  </body>
  </html>
  EOF_HTML
end


content = []

content << html_head

params = CGI.new

begin
  session = CGI::Session.new(params, {"new_session"=>false})
rescue ArgumentError
  session = nil
end

msg = params['msg'].to_s
send_url = params['send_url'].to_s

from_year_form0 = params['from_year_form0'].to_s
to_year_form0 = params['to_year_form0'].to_s
form0 = params['form0'].to_s
from_year_form1 = params['from_year_form1'].to_s
to_year_form1 = params['to_year_form1'].to_s
form1 = params['form1'].to_s
from_year_form2 = params['from_year_form2'].to_s
to_year_form2 = params['to_year_form2'].to_s
form2 = params['form2'].to_s
from_year_form3 = params['from_year_form3'].to_s
to_year_form3 = params['to_year_form3'].to_s
form3 = params['form3'].to_s
from_year_form4 = params['from_year_form4'].to_s
to_year_form4 = params['to_year_form4'].to_s
form4 = params['form4'].to_s
from_year_form5 = params['from_year_form5'].to_s
to_year_form5 = params['to_year_form5'].to_s
form5 = params['form5'].to_s
from_year_form6 = params['from_year_form6'].to_s
to_year_form6 = params['to_year_form6'].to_s
form6 = params['form6'].to_s
from_year_form7 = params['from_year_form7'].to_s
to_year_form7 = params['to_year_form7'].to_s
form7 = params['form7'].to_s
from_year_form8 = params['from_year_form8'].to_s
to_year_form8 = params['to_year_form8'].to_s
form8 = params['form8'].to_s
from_year_form9 = params['from_year_form9'].to_s
to_year_form9 = params['to_year_form9'].to_s
form9 = params['form9'].to_s

if session == nil
  session = CGI::Session.new(params, {"new_session"=>true})
else
  session = CGI::Session.new(params, {"new_session"=>true})
end

content << html_message(msg)

source_url_controller = SourceURLController.new
url_list = source_url_controller.list

content << html_url_table(url_list, send_url)

content << html_select_year(from_year_form0, to_year_form0, form0,
                            from_year_form1, to_year_form1, form1,
                            from_year_form2, to_year_form2, form2,
                            from_year_form3, to_year_form3, form3,
                            from_year_form4, to_year_form4, form4,
                            from_year_form5, to_year_form5, form5,
                            from_year_form6, to_year_form6, form6,
                            from_year_form7, to_year_form7, form7,
                            from_year_form8, to_year_form8, form8,
                            from_year_form9, to_year_form9, form9)


content << html_select_tables_and_graph

msg = "結果が表示できました．"

content << html_print_and_download(msg)

doc_info_controller = DocumentInfoController.new
document_html = doc_info_controller.get("/Users/masafumi/workspace/sdm/y-saori/documentlist.html")
document_informations = doc_info_controller.parse(document_html)

content << html_result

content << html_foot

puts content

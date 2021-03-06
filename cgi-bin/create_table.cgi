#!/usr/bin/ruby

require 'cgi'
require "cgi/escape"
require 'json'
require 'digest'
require "fileutils"
require 'securerandom'
require_relative '../lib/source_url_controller'
require_relative '../lib/document_info_controller'
require_relative '../lib/document_info'
require_relative '../lib/statistics_info'
require_relative '../lib/statistics_info_controller'


def html_head
  return <<~EOF_HTML
  Content-Type: text/html

  <html>
  <head>
  <title>文書管理統計表の閲覧・ダウンロード</title>
  <meta http-equiv="content-type" charset="utf-8">
  <link rel="stylesheet" href="../style.css">
  <script src="http://code.jquery.com/jquery-latest.min.js"></script>
  </head>
  <body>
  <center>
  <form action="create_table.cgi" method="POST">
  <font size=6>文書管理統計表の閲覧・ダウンロード</font>
  EOF_HTML
end

def html_message(msg)
  return <<~EOF_HTML
  <h3><font color="00CC00">#{msg}</font></h3>
  EOF_HTML
end
def html_url_table(url_list, send_url)
  pulldown_list = url_pulldown(send_url, url_list)
  return <<~EOF_HTML
  <p><font color=#CC0000>※登録済みのURLから一つ選択してください</font></p>
  <table border=1 bgcolor =#FFFFFF width="600">
  <tr>
    <td class="create_index">
      URL
    </td>
    <td>
      <select class="url_pull" name="send_url">
        #{pulldown_list}
      </select>
    </td>
  </tr>
  </table>
  EOF_HTML
end

def url_pulldown(send_url, url_list)
  pulldown_list = ""
  #pulldown_list << "<option value = #{send_url}>#{send_url}</option>\n"
  if send_url == ""
    pulldown_list << "<option value = "">""</option>\n"
  else
    for url_and_name in url_list
      if send_url == url_and_name["url"]
        content = "#{url_and_name["register_name"]}(#{url_and_name["url"]})"
        pulldown = "<option value = #{url_and_name["url"]}>#{content}</option>\n"
        pulldown_list << pulldown
        pulldown_list << "<option value = "">""</option>\n"
        break
      end
    end
  end

  for url_and_name in url_list
    content = "#{url_and_name["register_name"]}(#{url_and_name["url"]})"
    pulldown = "<option value = #{url_and_name["url"]}>#{content}</option>\n"
    pulldown_list << pulldown
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
    if forms[i] == "multiple"
      to_year_forms_type[i] = "text"
      waves[i] = "~"
    end
  end
end

  return <<~EOF_HTML
  <table border="1" width="600">
  <tr>
  <td class="create_index" rowspan="2">年度フィルタ</td>
  <td align="center">1つ追加 <button type="button" id="single_year_form">+</button></td>
  <td align="center">まとめて追加 <button type="button" id="multiple_year_form">+</button></td>
  </tr>

  <tr>
  <td colspan="2">
  <table>
  <tr>
  <td><input type="#{forms_type[0]}" name="form0" id="form0" value="#{form0}"></td>
  <td><input type="#{from_year_forms_type[0]}" name="from_year_form0" id="from_year_form0" value="#{from_year_form0}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2009"></td>
  <td><div id="form0_wave">#{waves[0]}</div></td>
  <td><input type="#{to_year_forms_type[0]}" name="to_year_form0" id="to_year_form0" value="#{to_year_form0}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2019"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[1]}" name="form1" id="form1" value='#{form1}'></td>
  <td><input type="#{from_year_forms_type[1]}" name="from_year_form1" id="from_year_form1" value="#{from_year_form1}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2010"></td>
  <td><div id="form1_wave">#{waves[1]}</div></td>
  <td><input type="#{to_year_forms_type[1]}" name="to_year_form1" id="to_year_form1" value="#{to_year_form1}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2020"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[2]}" name="form2" id="form2" value='#{form2}'></td>
  <td><input type="#{from_year_forms_type[2]}" name="from_year_form2" id="from_year_form2" value="#{from_year_form2}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2011"></td>
  <td><div id="form2_wave">#{waves[2]}</div></td>
  <td><input type="#{to_year_forms_type[2]}" name="to_year_form2" id="to_year_form2" value="#{to_year_form2}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2021"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[3]}" name="form3" id="form3" value='#{form3}'></td>
  <td><input type="#{from_year_forms_type[3]}" name="from_year_form3" id="from_year_form3" value="#{from_year_form3}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2012"></td>
  <td><div id="form3_wave">#{waves[3]}</div></td>
  <td><input type="#{to_year_forms_type[3]}" name="to_year_form3" id="to_year_form3" value="#{to_year_form3}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2022"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[4]}" name="form4" id="form4" value='#{form4}'></td>
  <td><input type="#{from_year_forms_type[4]}" name="from_year_form4" id="from_year_form4" value="#{from_year_form4}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2013"></td>
  <td><div id="form4_wave">#{waves[4]}</div></td>
  <td><input type="#{to_year_forms_type[4]}" name="to_year_form4" id="to_year_form4" value="#{to_year_form4}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2023"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[5]}" name="form5" id="form5" value='#{form5}'></td>
  <td><input type="#{from_year_forms_type[5]}" name="from_year_form5" id="from_year_form5" value="#{from_year_form5}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2014"></td>
  <td><div id="form5_wave">#{waves[5]}</div></td>
  <td><input type="#{to_year_forms_type[5]}" name="to_year_form5" id="to_year_form5" value="#{to_year_form5}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2024"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[6]}" name="form6" id="form6" value='#{form6}'></td>
  <td><input type="#{from_year_forms_type[6]}" name="from_year_form6" id="from_year_form6" value="#{from_year_form6}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2015"></td>
  <td><div id="form6_wave">#{waves[6]}</div></td>
  <td><input type="#{to_year_forms_type[6]}" name="to_year_form6" id="to_year_form6" value="#{to_year_form6}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2025"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[7]}" name="form7" id="form7" value='#{form7}'></td>
  <td><input type="#{from_year_forms_type[7]}" name="from_year_form7" id="from_year_form7" value="#{from_year_form7}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2016"></td>
  <td><div id="form7_wave">#{waves[7]}</div></td>
  <td><input type="#{to_year_forms_type[7]}" name="to_year_form7" id="to_year_form7" value="#{to_year_form7}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2026"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[8]}" name="form8" id="form8" value='#{form8}'></td>
  <td><input type="#{from_year_forms_type[8]}" name="from_year_form8" id="from_year_form8" value="#{from_year_form8}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2017"></td>
  <td><div id="form8_wave">#{waves[8]}</div></td>
  <td><input type="#{to_year_forms_type[8]}" name="to_year_form8" id="to_year_form8" value="#{to_year_form8}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2027"></td>
  </tr>
  <tr>
  <td><input type="#{forms_type[9]}" name="form9" id="form9" value='#{form9}'></td>
  <td><input type="#{from_year_forms_type[9]}" name="from_year_form9" id="from_year_form9" value="#{from_year_form9}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2018"></td>
  <td><div id="form9_wave">#{waves[9]}</div></td>
  <td><input type="#{to_year_forms_type[9]}" name="to_year_form9" id="to_year_form9" value="#{to_year_form9}" size="4" maxlength="4" pattern="[0-9]{4}" placeholder="例) 2028"></td>
  </tr>
  </table>
  </td>
  </tr>

  </table>
  <div id="year_form_field"></div>
  </table>
  <script>
//  window.onload = function(){
    document.getElementById("single_year_form").onclick = function(){
      for(let i = 0; i < 10; i++){
        if(document.getElementById("form"+i).value == ""){
          document.getElementById("form"+i).value = "single";
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
          document.getElementById("form"+i).value = "multiple";
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
      if(document.getElementById("form"+i).value == "single" || document.getElementById("form"+i).value == "multiple"){
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

def html_select_tables_and_graph(single_select, multiple_select, graph_select)
  return <<~EOF_HTML
  <p><font color=#CC0000>※表示またはダウンロードしたい作成物を選択してください</font></p>
  <table border="1" width="600">
  <tr>
  <td rowspan="3" class="create_index">作成物</td>
  <td align="center"><input name="single_select" id="single_select" type="checkbox" value='#{single_select}'></td>
  <td>提出回数集計表</td>
  </tr>
  <tr>
  <td align="center"><input name="multiple_select" id="multiple_select" type="checkbox" value='#{multiple_select}'></td>
  <td>平均提出回数比較表</td>
  </tr>
  <tr>
  <td align="center"><input name="graph_select" id="graph_select" type="checkbox" value='#{graph_select}'></td>
  <td>平均提出回数比較グラフ</td>
  </tr>
  </table>

  <script>
  if(document.getElementById("single_select").value == "checked"){
    document.getElementById("single_select").checked = true;
  }else{
    document.getElementById("single_select").value = ""
  }
  if(document.getElementById("multiple_select").value == "checked"){
    document.getElementById("multiple_select").checked = true;
  }else{
    document.getElementById("multiple_select").value = ""
  }
  if(document.getElementById("graph_select").value == "checked"){
    document.getElementById("graph_select").checked = true;
  }else{
    document.getElementById("graph_select").value = ""
  }

  function value_to_nil(){
    if (this.checked){
      this.value = "checked"
      }else{
      this.value = ""
    }
  }

  var single = document.getElementById("single_select");
  var multiple = document.getElementById("multiple_select");
  var graph = document.getElementById("graph_select");
  single.onclick = value_to_nil
  multiple.onclick = value_to_nil
  graph.onclick = value_to_nil
  </script>
  EOF_HTML
end

def html_print_and_download(print_select, download_select, update_select, msg, used_url)
  return <<~EOF_HTML
  <input name="msg" type="hidden" value="#{msg}">
  <input name="used_url" type="hidden" value="#{used_url}">  
  <input name="print_select" id="print_select" type="hidden" value="#{print_select}"/>
  <input name="download_select" id="download_select" type="hidden" value="#{download_select}"/>
  <p><input name="update_select" id="update_select" type="checkbox" value='#{update_select}'>最新の文書管理情報を取得</p>
  <table border="0">
  <tr>
  <td><input id="print" type="submit" value="表示"></td>
  <td><input id="download" type="submit" value="ダウンロード"></td>
  </tr>
  </table>

  <script>
  document.getElementById("print").onclick = function() {
    document.getElementById("print_select").value = "click";
    document.getElementById("download_select").value = "";
  }
  document.getElementById("download").onclick = function() {
    document.getElementById("download_select").value = "click";
    document.getElementById("print_select").value = "";
  }

  if(document.getElementById("update_select").value == "checked"){
    document.getElementById("update_select").checked = true;
  }else{
    document.getElementById("update_select").value = ""
  }

  function value_to_nil(){
    if (this.checked){
      this.value = "checked"
    }else{
      this.value = ""
    }
  }

  var update = document.getElementById("update_select");
  update.onclick = value_to_nil;
</script>
  EOF_HTML
end

def html_basic_dialog(username, password)
  return <<~EOF_HTML
  <input type="hidden" id="username" name="username" value="#{username}">
  <input type="hidden" id="password" name="password" value="#{password}">

  <script>
  var name = prompt("名前を入力してください");
  var pass = prompt("パスワードを入力してください");
  console.log(name)
  document.getElementById('username').value = name;
  document.getElementById('password').value = pass;
  if(document.getElementById("print_select").value == "click") {
    document.getElementById("print").click();
  }else if(document.getElementById("download_select").value == "click") {
    document.getElementById("download").click();
  }
   </script>
  EOF_HTML
end

def html_download_script(cgi_filename, download_filename, download_directory)
  return <<~EOF_HTML
  <script>
  function downloadFromUrlAutomatically(url, fileName){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';
    xhr.onload = function(e){
      if(this.status == 200){
        var urlUtil = window.URL || window.webkitURL;
        var imgUrl = urlUtil.createObjectURL(this.response);
        var link = document.createElement('a');
        link.href=imgUrl;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link)
      }
    };
    xhr.send();
  }

  downloadFromUrlAutomatically('#{cgi_filename}', "#{download_filename}");
  </script>

  EOF_HTML
end

def html_foot
  return <<~EOF_HTML
  <a href="../index.html">TOPへ戻る</a>
  </form>
  </center>
  </body>
  </html>
  EOF_HTML
end


content = []


params = CGI.new

msg = CGI.escapeHTML(params['msg'].to_s)
send_url = CGI.escapeHTML(params['send_url'].to_s)

from_year_form0 = CGI.escapeHTML(params['from_year_form0'].to_s)
to_year_form0 = CGI.escapeHTML(params['to_year_form0'].to_s)
form0 = CGI.escapeHTML(params['form0'].to_s)
from_year_form1 = CGI.escapeHTML(params['from_year_form1'].to_s)
to_year_form1 = CGI.escapeHTML(params['to_year_form1'].to_s)
form1 = CGI.escapeHTML(params['form1'].to_s)
from_year_form2 = CGI.escapeHTML(params['from_year_form2'].to_s)
to_year_form2 = CGI.escapeHTML(params['to_year_form2'].to_s)
form2 = CGI.escapeHTML(params['form2'].to_s)
from_year_form3 = CGI.escapeHTML(params['from_year_form3'].to_s)
to_year_form3 = CGI.escapeHTML(params['to_year_form3'].to_s)
form3 = CGI.escapeHTML(params['form3'].to_s)
from_year_form4 = CGI.escapeHTML(params['from_year_form4'].to_s)
to_year_form4 = CGI.escapeHTML(params['to_year_form4'].to_s)
form4 = CGI.escapeHTML(params['form4'].to_s)
from_year_form5 = CGI.escapeHTML(params['from_year_form5'].to_s)
to_year_form5 = CGI.escapeHTML(params['to_year_form5'].to_s)
form5 = CGI.escapeHTML(params['form5'].to_s)
from_year_form6 = CGI.escapeHTML(params['from_year_form6'].to_s)
to_year_form6 = CGI.escapeHTML(params['to_year_form6'].to_s)
form6 = CGI.escapeHTML(params['form6'].to_s)
from_year_form7 = CGI.escapeHTML(params['from_year_form7'].to_s)
to_year_form7 = CGI.escapeHTML(params['to_year_form7'].to_s)
form7 = CGI.escapeHTML(params['form7'].to_s)
from_year_form8 = CGI.escapeHTML(params['from_year_form8'].to_s)
to_year_form8 = CGI.escapeHTML(params['to_year_form8'].to_s)
form8 = CGI.escapeHTML(params['form8'].to_s)
from_year_form9 = CGI.escapeHTML(params['from_year_form9'].to_s)
to_year_form9 = CGI.escapeHTML(params['to_year_form9'].to_s)
form9 = CGI.escapeHTML(params['form9'].to_s)

print_select = CGI.escapeHTML(params['print_select'].to_s)
download_select = CGI.escapeHTML(params['download_select'].to_s)
update_select = CGI.escapeHTML(params['update_select'].to_s)

single_select = CGI.escapeHTML(params['single_select'].to_s)
multiple_select = CGI.escapeHTML(params['multiple_select'].to_s)
graph_select = CGI.escapeHTML(params['graph_select'].to_s)

username = CGI.escapeHTML(params['username'].to_s)
password = CGI.escapeHTML(params['password'].to_s)

used_url = CGI.escapeHTML(params['used_url'].to_s)

doc_info_controller = DocumentInfoController.new
statistics_info_controller = StatisticsInfoController.new
statistics_table_result = ""
download_result = ""
download_directory = ""

if send_url == "" && (print_select == "click" || download_select == "click")
  msg = "URLを選択してください．"
end

if send_url != ""
  if send_url != used_url || update_select == "checked" # 初めてのURLにアクセスするとき，もしくは更新のチェックボックスが選択されているとき
    begin
      document_html = doc_info_controller.get(send_url, username, password)
      document_informations = doc_info_controller.parse(document_html)
      hash = []
      if document_informations != []
        document_informations.each do |info|
          new_hash = {"group" => info.group, "remarks" => info.remarks}
          hash.push(new_hash)
        end
        url_hash = Digest::SHA256.hexdigest(send_url).encode("UTF-8")
        File.open("../database/#{url_hash}.json", 'w') do |file|
          file.flock(File::LOCK_EX)
          pretty = JSON.pretty_generate(hash)
          file.puts pretty
        end
      end
    rescue OpenURI::HTTPError  # 401 authorization required のとき
      basic_flag = 1
    rescue Errno::ENOENT, SocketError # 選択したURLが存在しないとき
    end
  elsif send_url == used_url # 前回と同じURLにアクセスするとき
    document_informations = []
    url_hash = Digest::SHA256.hexdigest(send_url).encode("UTF-8")
    hash = File.open("../database/#{url_hash}.json", 'r') do |file|
      JSON.load(file)
    end
    hash.each do |v|
      document_informations.push(DocumentInfo.new(v["group"], v["remarks"]))
    end
  end
  if document_informations == nil # URLにアクセスできないとき
    msg = "選択したURLにはアクセスできません．存在しないURLにアクセスしている可能性があります．"
  elsif document_informations == [] # 選択したURLが文書管理システムではないとき
    msg = "文書管理情報が取得できません．選択したアクセス先が文書管理システムではない可能性があります．"
  else # 文書管理システムにアクセスできたとき
    $statistics_year = []
    years = []
    forms = [form0, form1, form2, form3, form4, form5, form6, form7, form8, form9]
    from_year_forms = [from_year_form0, from_year_form1, from_year_form2, from_year_form3, from_year_form4, from_year_form5, from_year_form6, from_year_form7, from_year_form8, from_year_form9]
    to_year_forms = [to_year_form0, to_year_form1, to_year_form2, to_year_form3, to_year_form4, to_year_form5, to_year_form6, to_year_form7, to_year_form8, to_year_form9]
    # 年度入力フォームに何も入力されていないとき
    if form0 == "" && form1 == "" && form2 == "" && form3 == "" && form4 == "" &&
      form5 == "" && form6 == "" && form7 == "" && form8 == "" && form9 == ""
      for i in 2000 .. 2100
        years.push(i)
      end
    else # 年度選択がされているとき
      forms.each_with_index do |form, i|
        if form == "single" && from_year_forms[i] != ""
          years.push(from_year_forms[i].to_i)
        elsif form == "multiple"
          if from_year_forms[i] != "" && to_year_forms[i] != ""
            for i in from_year_forms[i].to_i .. to_year_forms[i].to_i
              years.push(i)
            end
          elsif from_year_forms[i] != ""
            for i in from_year_forms[i].to_i .. 2100
              years.push(i)
            end
          elsif to_year_forms[i] != ""
            for i in 2000 .. to_year_forms[i].to_i
              years.push(i)
            end
          end
        end
      end
    end
    years = years.uniq # 年度の重複を取り除く
    years = years.sort # 年度を昇順に並び替える
    years.each do |select_year|
      $statistics_year.push(StatisticsInfo.new(0,0,0,0,0,0,select_year))
    end

    for document_information in document_informations
      statistics_info_controller.push(document_information.group, document_information.remarks)
      doc_info_controller.update_url(send_url)
    end

    # 使われていない年度を削除
    $statistics_year.each do |single_year|
      if single_year.product_number == []
        years.delete(single_year.year)
      end
    end
    $statistics_year.delete_if do |single_year|
      single_year.product_number == []
    end

    if years == [] # 表示できる年度がないとき
      msg = "選択した年度は表示できません．"
    elsif single_select == "" && multiple_select == "" && graph_select == "" # 作成物を選択していないとき
      msg = "一つ以上の作成物を選択してください．"
    else
      if print_select == "click"
        if single_select == "checked"
          single_year_table = []
          $statistics_year.each do |single_year|
            single_year_table.push(statistics_info_controller.create_single_year_table(single_year.product_number, single_year.product_name, single_year.group_name, single_year.submission_number, single_year.submission_average, single_year.submission_sum, 2009))
          end
        end

        if multiple_select == "checked"
          group_name_len = 0
          i_tmp = 0
          $statistics_year.each_with_index do |single_year, i|
            if group_name_len < single_year.group_name.length
              i_tmp = i
              group_name_len = single_year.group_name.length
            end
          end
          multiple_year_table = statistics_info_controller.create_multiple_years_table($statistics_year[i_tmp].group_name, $statistics_year[i_tmp].submission_average, 2009)
        end

        graph_file_name = ""
        if graph_select == "checked"
          if download_directory == ""
            download_directory = SecureRandom.uuid
            FileUtils.mkdir("../downloads/#{download_directory}")
          end
          group_name_len = 0
          i_tmp = 0
          $statistics_year.each_with_index do |single_year, i|
            if group_name_len < single_year.group_name.length
              i_tmp = i
              group_name_len = single_year.group_name.length
            end
          end
          graph_file_name = statistics_info_controller.create_graph($statistics_year[i_tmp].group_name, $statistics_year[i_tmp].submission_average, years, download_directory)
        end
        statistics_table_result = statistics_info_controller.print_table(single_year_table, multiple_year_table, graph_file_name, download_directory)
      end

      if download_select == "click"
        single_year_file_name = []
        if single_select == "checked"
          if download_directory == ""
            download_directory = SecureRandom.uuid
            FileUtils.mkdir("../downloads/#{download_directory}")
          end
          single_year_table = []
          $statistics_year.each do |single_year|
            single_year_table.push(statistics_info_controller.create_single_year_table(single_year.product_number, single_year.product_name, single_year.group_name, single_year.submission_number, single_year.submission_average, single_year.submission_sum, single_year.year))
          end
          single_year_table.zip($statistics_year) do |single_year, a|
            single_year_file_name.push(statistics_info_controller.create_single_year_csv_file(single_year, a.year, download_directory))
          end
        end

        multiple_year_file_name = ""
        if multiple_select == "checked"
          if download_directory == ""
            download_directory = SecureRandom.uuid
            FileUtils.mkdir("../downloads/#{download_directory}")
          end
          group_name_len = 0
          i_tmp = 0
          $statistics_year.each_with_index do |single_year, i|
            if group_name_len < single_year.group_name.length
              i_tmp = i
              group_name_len = single_year.group_name.length
            end
          end
          multiple_year_table = statistics_info_controller.create_multiple_years_table($statistics_year[i_tmp].group_name, $statistics_year[i_tmp].submission_average, 2009)
          multiple_year_file_name = statistics_info_controller.create_multiple_years_csv_file(multiple_year_table, download_directory)
        end

        graph_file_name = ""
        if graph_select == "checked"
          if download_directory == ""
            download_directory = SecureRandom.uuid
            FileUtils.mkdir("../downloads/#{download_directory}")
          end
          group_name_len = 0
          i_tmp = 0
          $statistics_year.each_with_index do |single_year, i|
            if group_name_len < single_year.group_name.length
              i_tmp = i
              group_name_len = single_year.group_name.length
            end
          end
          graph_file_name = statistics_info_controller.create_graph($statistics_year[i_tmp].group_name, $statistics_year[i_tmp].submission_average, years, download_directory)
        end

        download_filename = statistics_info_controller.download_table(single_year_file_name, multiple_year_file_name, graph_file_name, download_directory)
        if download_filename.include?(".zip")
          download_result = html_download_script("download_zip.cgi?download_directory=#{download_directory}", download_filename, download_directory)
        elsif download_filename.include?(".png")
          download_result = html_download_script("view_graph.cgi?download_directory=#{download_directory}", download_filename, download_directory)
        elsif download_filename.include?(".csv")
          download_result = html_download_script("download_csv.cgi?download_directory=#{download_directory}&download_filename=#{download_filename}", download_filename, download_directory)
        end
      end
      msg = "結果が表示できました．"
      used_url = send_url # 選択したURLが文書管理システムであるとき，使用したURLを記録する．
    end
  end
end

source_url_controller = SourceURLController.new
url_list = source_url_controller.list

content << html_head


begin
  if basic_flag == 1
    if username != "" || password != "" # 認証情報が間違えているとき
      username = ""
      password = ""
      msg = "認証に失敗しました．"
    else # 認証情報を入力するダイアログを表示
      basic_dialog = html_basic_dialog(username, password)
    end
  end
end

content << html_message(msg)

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

content << html_select_tables_and_graph(single_select, multiple_select, graph_select)

content << html_print_and_download(print_select, download_select, update_select, msg, used_url)


begin
  content << basic_dialog
end

if statistics_table_result != ""
  content << statistics_table_result
end

if download_result != ""
  content << download_result
end

content << html_foot

puts content

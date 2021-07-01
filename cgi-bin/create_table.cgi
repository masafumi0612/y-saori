#!/usr/bin/ruby

require 'cgi'
require 'cgi/session'
#require '../lib/source_url_controller.rb'

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

def html_url_table(url_list)
  pulldown_list = url_pulldown(url_list)
  return <<~EOF_HTML
  <p><font color=#CC0000>※登録済みのURLから一つ選択してください</font></p>
  <table border=1 bgcolor =#FFFFFF>
  <tr>
    <td bgcolor =#CCFFFF>
      URL
    </td>
    <td>
      <select name="url">
        #{pulldown_list}
      </select>
    </td>
  </tr>
  </table>
  EOF_HTML
end

def html_select_year(from_year_form, to_year_form = nil, year = nil)
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
  <td><input type=#{year[0]} name="year[0]" id="year[0]"></td>
  <td><input type=#{from_year_form[0]} name="from_year_form[0]" id="from_year_form[0]">
  <td><input type=#{from_year_form[0]} name="from_year_form[0]" id="from_year_form[0]">
  </tr>
  </table>
  <table border="1">
  <div id="year_form_field"></div>
  </table>
  <script>
//  window.onload = function(){
    document.getElementById("single_year_form").onclick = function(){
      var row = document.createElement("tr");
      var cell = document.createElement("td");
      var checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = "year_checkbox";
      checkbox.checked="checked";
      var year_form = document.createElement("input");
      year_form.type = "text";
      year_form.id = "uComment";
      year_form.name = "uComment";
      cell.appendChild(checkbox);
      cell.appendChild(year_form);
      row.appendChild(cell);
      document.getElementById("year_form_field").appendChild(row);
    }

    document.getElementById("multiple_year_form").onclick = function(){
      var row = document.createElement("tr");
      var cell = document.createElement("td");
      var checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = "year_checkbox";
      checkbox.checked="checked";
      var year_start_form = document.createElement("input");
      year_start_form.type = "text";
      year_start_form.id = "uComment";
      year_start_form.name = "uComment";
      var wave = document.createTextNode("~");
      var year_end_form = document.createElement("input");
      year_end_form.type = "text";
      year_end_form.id = "uComment";
      year_end_form.name = "uComment";
      cell.appendChild(checkbox);
      cell.appendChild(year_start_form);
      cell.appendChild(wave);
      cell.appendChild(year_end_form);
      row.appendChild(cell);
      document.getElementById("year_form_field").appendChild(row);
    }

    function remove_year(){
      if (this.checked){
      }else{
        console.log($(this));
       $(this).type = "hidden";
      }
    }
/*    var years = document.getElementsByName("test");
    console.log(years);
    for(let i=0; i<10;i++){
      years[0].onclick = remove_year
    }*/
//  }
  </script>
  EOF_HTML
end

def html_select_year_test(msg)
  return <<~EOF_HTML
  <ul>
  <li><input type="checkbox" checked="checked" name="test" id="test77" /> - らっぱ</li>
  <li><input type="checkbox" checked="checked" name="test" id="test2" /> - りんご</li>
  <li><input type="checkbox" id="test3" name="year_checked3"/> - ごりら</li>
  <li><input type="checkbox" checked="checked" name="test" id="test4" /></li>
  </ul>
  <table border="1">
  <tr>
  <td><input type="checkbox" checked="checked" name="test" id="test1" /></td>
  <td><input type="form" checked="checked" name="msg" id="test1_form" value=""></td>
  </tr>
  </table>
  <script>

  function remove_name_test(){
    if (this.checked){
    }else{
      this.type = "hidden";
      console.log(document.getElementById(this.id+"_form"));
//      document.getElementById(this.id+"_form").type = "hidden";
      document.getElementById(this.id+"_form").value = "こんにちは";
      }
    }

    for(let i = 1; i < 3; i++){
      document.getElementById("test"+i).onclick = remove_name_test;
    }
  </script>
  EOF_HTML
end

def url_pulldown(url_list)
  pulldown_list = ""
  pulldown_list << "<option value = 1>""</option>\n"
  for url_and_name in url_list
    content = "#{url_and_name["url_name"]}(#{url_and_name["url"]})"
    pulldown = "<option value = 1>#{content}</option>\n"
    pulldown_list << pulldown
  end
  return pulldown_list
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
  <input name="msg" type="text" value="#{msg}">
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

#session = CGI::Session.new(params)

msg = params['msg'].to_s

from_year_form = params['form_year_form']
to_year_form = params['to_year_form']
year = params['year']

from_year_form = ["hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden"]
to_year_form = ["hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden"]
year = ["hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden","hidden"]


content << html_message(msg)

url_list = [{"url"=>"http://sdm.swlab.cs.okayama-u.ac.jp/2012/cgi-bin/documentlist.cgi", "url_name"=>"文書管理システム"}, {"url"=>"http://sdm2.swlab.cs.okayama-u.ac.jp/2012/cgi-bin/documentlist.cgi", "url_name"=>"文書管理システム2"}]

content << html_url_table(url_list)

content << html_select_year(from_year_form, to_year_form, year)
#content << html_select_year_test(msg)

content << html_select_tables_and_graph

content << html_print_and_download(msg)

#puts "session"
#puts session
#if session != nil
content << html_result
#end

content << html_foot

puts content

#!/usr/bin/ruby

require 'cgi'
#require '../lib/source_url_controller.rb'

def html_head
  return <<~EOF_HTML
  Content-Type: text/html

  <html>
  <head>
  <title>文書管理統計表の閲覧・ダウンロード</title>
  <meta http-equiv="content-type" charset="utf-8">
  </head>
  <body>
  <center>
  <font size=6>文書管理統計表の閲覧・ダウンロード</font>
    <h3>メッセージ欄</h3>
  EOF_HTML
end

def html_foot
  return <<~EOF_HTML
  <a href="../html/index.html">トップへ戻る</a>
  </center>
  </body>
  </html>
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
  <table border=0 bgcolor =#FFFFFF>
  <tr bgcolor =#FFCCFF>
  <tr>
    <th>
      URL
    </th>
    <th>
      <select  name="url">
        #{pulldown_list}
      </select>
    </th>
  </tr>
  </table>
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

content = []

content << html_head

params = CGI.new

msg = params['msg'].to_s
msg = "これはテストメッセージです．"

content << html_message(msg)

url_list = [{"url"=>"http://sdm.swlab.cs.okayama-u.ac.jp/2012/cgi-bin/documentlist.cgi", "url_name"=>"文書管理システム"}, {"url"=>"http://sdm2.swlab.cs.okayama-u.ac.jp/2012/cgi-bin/documentlist.cgi", "url_name"=>"文書管理システム2"}]

content << html_url_table(url_list)

content << html_foot

puts content

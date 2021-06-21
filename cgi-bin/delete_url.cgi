#!/usr/bin/ruby

#rubyのexeファイルを実行時に指定すること

#puts "Content-type: text/html\n\n"; #\n\nを加えないとエラーになってしまう(ログを見て確認)

require 'cgi'

def html_head
    return <<~EOF_HTML
    Content-Type: text/html
  
    <html>
    <head>
    <title>文書管理情報取得元削除</title>
    <meta http-equiv="content-type" charset="utf-8">
    </head>
    EOF_HTML
end

def html_body
    return <<~EOF_HTML
    <center>
    <body>
    <font size=6>文書管理情報取得元削除</font>
      <h3>メッセージ欄</h3>
    </body>
    </center>
    EOF_HTML
end

def html_foot
    return <<~EOF_HTML
    <a href="../html/index.html">トップへ戻る</a>
    </body>
    </html>
    EOF_HTML
  end


content = []

content << html_head
content << html_body
content << html_foot

puts content

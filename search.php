<?php
header("Content-type: text/plain; charset=UTF-8");

// フォームから検索文字列を受け取る
$query = $_GET['query'];

// Python実行コマンド
$command = "C:\anaconda3\python.exe C:\\xampp\htdocs\python\scraping.py";

// 実行コマンド整形(実行コマンド + 検索クエリ)
$command = $command." \"".$query."\"";

// クエリをPythonに渡す
exec($command, $output, $result);

// JSへPythonからの取得結果を渡す
echo $output[0];
?>
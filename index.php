<!DOCTYPE html>
<html lang="ja">
	<head>
		<meta charset="UTF-8">
		<!-- CSS -->
		<link rel="stylesheet" type="text/css" href="style.css">
		<!-- Google Fonts -->
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Shrikhand&display=swap" rel="stylesheet">
		<!-- JS -->
		<!-- jQuery -->
		<script src="jquery-3.6.0.min.js"></script>
		<!-- SweetAlert -->
		<script src="https://cdn.jsdelivr.net/npm/sweetalert2@8"></script>
		<!-- main.js -->
		<script type="text/javascript" src="main.js"></script>
		<!-- viewport設定 -->
		<meta name=”viewport” content=”width=device-width, initial-scale=1”>
		<title>JSONファイル受け渡しテスト</title>		
	</head>
	<body>
		<!-- タイトルバー -->
		<header>
			<div id="title">
				<h1 class="title">JSONファイル受け渡しテスト</h1>
			</div>
			<!-- あいさつ -->
			<div id="greeting">
				<p class="greeting"></p>
			</div>
			<!-- ログイン/ログアウト/登録ボタン -->
			<div id="buttons">
			</div>
		</header>
		<!-- コンテンツ -->
		<div class="contains">
			<!-- 検索ウィンドウ -->
			<form class="search_container">
				<input type="text" name="query" placeholder="キーワード検索">
				<button type="button" class="search">検索</button>
			</form>
			<!-- 検索結果説明 -->
			<li id="result_description"></li>
			<!-- 検索履歴 -->
			<li id="items"></li>
		</div>
		<!-- フッター -->
		<footer>
			<p class="footer">© 2022</p>
		</footer>
		</div>
	</body>
</html>
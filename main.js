// 定数一覧
const SEARCHING = '検索中'
const SEARCH_COMPLETE = '検索完了'
const SEARCHING_DESCRIPTION = 'この処理には時間がかかることがあります。'
const RESULT_ZERO = '検索結果は0件でした。'
const INPUT_NULL = '検索ワードが<br>入力されていません。'
const PROCESSING_RESULT_0 = 0;
const PROCESSING_RESULT_1 = 1;
const PROCESSING_RESULT_2 = 2;
const YAHOO_AUCTION = "YAHOO_AUCTION"
const EBAY = "EBAY"
const AMAZON = "AMAZON"
const ICON_YAHOO = "/image/icon_yahoo.png"
const ICON_EBAY = "/image/icon_ebay.png"
const ICON_AMAZON = "/image/icon_amazon.png"

async function SearchAjax(){
    // 処理時間計測 開始
    var start = performance.now();
    // JSONフォーマット受け渡し処理
    var data = {
      'query' : $query,
    };
    await $.get({
      type: 'get',
      url: "search.php",
      data: data,
      dataType: 'json'
    }).then(
      function(result){
        AfterAjax(result,start);
      }
    )
  }
  // 連想配列のNULLチェック
  function isEmpty(obj){
    return !Object.keys(obj).length;
  }

  function AfterAjax(data,start){
    console.log(data);
    // 取得結果を表示
    $json_array_number = 0;
    let element = document.getElementById('items');
    let element2 = document.getElementById('result_description');

    // 検索結果がすでに存在する場合は初期化する
    if(element.innerText){
      element.innerText = "";
      element2.innerText = "";
    }

    //検索結果が0件の場合
    if(isEmpty(data)){
      Swal.fire({
        title: RESULT_ZERO,
        type : 'error',
        confirmButtonText: 'OK',
        focusConfirm: false,
      })
    }
    else{
      for (json_array_number=0; json_array_number < data.length; json_array_number++) {

        switch(data[json_array_number].source){
          case YAHOO_AUCTION:
            icon_image = ICON_YAHOO;
            element.insertAdjacentHTML('beforeend', '<div class="card">  <a href="' + data[json_array_number].url + '" target="_blank"><img src="' + data[json_array_number].image + '"><div class="card_icon"><img src="' + icon_image + '"></div><div class="card_price-container1">現在:' + data[json_array_number].price1 + '</div><div class="card_price-container2">即決:' + data[json_array_number].price2 + '</div><div class="card_access">掲載元へ</div><p class="card_title">' + data[json_array_number].name + '</p></a><button><div class="card_favorite">♥</div></div></button>');
            break;
          case EBAY:
            icon_image = ICON_EBAY;
            element.insertAdjacentHTML('beforeend', '<div class="card">  <a href="' + data[json_array_number].url + '" target="_blank"><img src="' + data[json_array_number].image + '"><div class="card_icon"><img src="' + icon_image + '"></div><div class="card_price-container1">現在:' + data[json_array_number].price1 + '</div><div class="card_price-container2">即決:' + data[json_array_number].price2 + '</div><div class="card_access">掲載元へ</div><p class="card_title">' + data[json_array_number].name + '</p></a><div class="card_favorite">♥</div></div>');
            break;
          case AMAZON:
            icon_image = ICON_AMAZON;
            element.insertAdjacentHTML('beforeend', '<div class="card">  <a href="' + data[json_array_number].url + '" target="_blank"><img src="' + data[json_array_number].image + '"><div class="card_icon"><img src="' + icon_image + '"></div><div class="card_price-container2">価格:' + data[json_array_number].price1 + '</div><div class="card_access">掲載元へ</div><p class="card_title">' + data[json_array_number].name + '</p></a><div class="card_favorite">♥</div></div>');
            break;
        }
      }
    }
    // 処理時間計測 終了
    var end = performance.now();
    processing_time = end - start;
    // ミリ秒を秒に変換
    processing_time /= 1000;
    processing_time = processing_time.toFixed(1);

    element2.insertAdjacentHTML('beforeend', '検索件数:' + data.length + '件<br>検索処理時間:' + processing_time + '秒<br>');
    $("#result_description").css({
      "display" : "flex"
    })

    // 処理時間計測用変数の初期化
    start = 0;
    end = 0;
    MsgSearchComplete();

    return true
  }

  // 検索完了アラート
  function MsgSearchComplete(){
    Swal.fire({
    title: SEARCH_COMPLETE,
    html: SEARCH_COMPLETE,
    focusConfirm: false,
    showConfirmButton :false,
    type : 'success',
    timer : '1000'
    })
  }
  // 検索中アラート
  function MsgSearching(){
    Swal.fire({
      title: SEARCHING,
      html: SEARCHING_DESCRIPTION,
      focusConfirm: false,
      showConfirmButton :false,
      allowOutsideClick : false,
      allowEscapeKey : true,
      onBeforeOpen: () => {
        Swal.showLoading();
      }
    })
  }

  // 空入力値アラート
  function InputNullMsg(){
    Swal.fire({
      title: INPUT_NULL,
      type : 'warning',
      confirmButtonText: 'OK',
      focusConfirm: false,
    })
  }

  // 検索実行
  $(document).on('click','.search', function () {
    // 入力値取得
    $query = document.querySelector("input[name=query]").value;

    if(!$query){
      InputNullMsg();
    }
    else{
      MsgSearching();
      SearchAjax();
    }
  });
//画像の縦横の大きさ（ピクセル）
let imageWidth
let imageHeight
// 0,1,2でループさせる
let point = 0

const myPics = document.getElementById('canvasArea')
const canvas = document.getElementById("canvasArea")
const ctx = canvas.getContext('2d')


//マウスボタンクリックイベント
myPics.addEventListener('mousedown', e => {
  x = e.offsetX;
  y = e.offsetY;
  if (point == 0) { // 1ポイント目を設定.
    //P0に表示
    document.getElementById("point0X").innerHTML = x
    document.getElementById("point0Y").innerHTML = y
    document.getElementById("point0XNormalize").innerHTML = x / imageWidth
    document.getElementById("point0YNormalize").innerHTML = y / imageHeight
    point = 1
  } else if (point == 1) {  // 2ポイント目を設定して描画
    //P3に表示
    document.getElementById("point3X").innerHTML = x
    document.getElementById("point3Y").innerHTML = y
    document.getElementById("point3XNormalize").innerHTML = x / imageWidth
    document.getElementById("point3YNormalize").innerHTML = y / imageHeight
    //色を設定
    ctx.strokeStyle = "red";
    //描画する
    ctx.strokeRect(
      Math.min(document.getElementById("point0X").innerHTML, document.getElementById("point3X").innerHTML),
      Math.min(document.getElementById("point0Y").innerHTML, document.getElementById("point3Y").innerHTML),
      Math.abs(document.getElementById("point0X").innerHTML - document.getElementById("point3X").innerHTML),
      Math.abs(document.getElementById("point0Y").innerHTML - document.getElementById("point3Y").innerHTML)
    )
    point = 2
  } else {  // 表示をリセット.
    //描画をクリア
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0)
    point = 0
  }
});

//マウスの移動イベント
myPics.addEventListener('mousemove', e => {
  x = e.offsetX;
  y = e.offsetY;
  document.getElementById("xPosition").innerHTML = x
  document.getElementById("yPosition").innerHTML = y
  document.getElementById("xPositionNormalize").innerHTML = x / imageWidth
  document.getElementById("yPositionNormalize").innerHTML = y / imageHeight
});


let img = new Image();
img.src = document.getElementsByName("imagePath")[0].value

//画像をオンロードした後に実行する
img.onload = function () {
  // 画像のサイズを取得する
  imageWidth = img.naturalWidth;
  imageHeight = img.naturalHeight;


  //キャンバスを画像サイズに設定
  document.getElementById("canvasArea").setAttribute("width", imageWidth)
  document.getElementById("canvasArea").setAttribute("height", imageHeight)

  //画像をcanvasに描画
  ctx.drawImage(img, 0, 0)
}


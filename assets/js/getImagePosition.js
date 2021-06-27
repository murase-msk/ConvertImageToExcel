//画像の縦横の大きさ（ピクセル）
let imageWidth
let imageHeight
// 前にクリックした位置
let prevX
let prevY
// 0,1,2でループさせる
let point = 0

const myPics = document.getElementById('canvasArea')
const canvas = document.getElementById("canvasArea")
const ctx = canvas.getContext('2d')


//マウスボタンクリックイベント
myPics.addEventListener('mousedown', e => {
  x = e.offsetX;
  y = e.offsetY;
  if (point == 0) { // 1ポイント目をprevに入れる.
    prevX = x
    prevY = y
    point = 1
  } else if (point == 1) {  // １ポイント目と2ポイント目からP0,P3を設定して描画
    //P0に表示
    document.getElementById("point0X").innerHTML = Math.min(x, prevX)
    document.getElementById("point0Y").innerHTML = Math.min(y, prevY)
    document.getElementsByClassName("point0XNormalize")[0].innerHTML = Math.min(x / imageWidth, prevX / imageWidth)
    document.getElementsByClassName("point0XNormalize")[1].innerHTML = Math.min(x / imageWidth, prevX / imageWidth)
    document.getElementsByClassName("point0YNormalize")[0].innerHTML = Math.min(y / imageWidth, prevY / imageWidth)
    document.getElementsByClassName("point0YNormalize")[1].innerHTML = Math.min(y / imageWidth, prevY / imageWidth)
    //P3に表示
    document.getElementById("point3X").innerHTML = Math.max(x, prevX)
    document.getElementById("point3Y").innerHTML = Math.max(y, prevY)
    document.getElementsByClassName("point3XNormalize")[0].innerHTML = Math.max(x / imageWidth, prevX / imageWidth)
    document.getElementsByClassName("point3XNormalize")[1].innerHTML = Math.max(x / imageWidth, prevX / imageWidth)
    document.getElementsByClassName("point3YNormalize")[0].innerHTML = Math.max(y / imageWidth, prevY / imageWidth)
    document.getElementsByClassName("point3YNormalize")[1].innerHTML = Math.max(y / imageWidth, prevY / imageWidth)
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


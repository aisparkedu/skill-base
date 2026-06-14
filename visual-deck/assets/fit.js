/* 单页等比缩放 + 居中。
   定尺 .slide 比视口大时，靠 JS 显式 translate 居中（transform-origin:top left），
   ⚠ 不依赖 body 的 flex 居中——视口比 slide 窄(如 1366/1280 笔记本)时，flex 处理溢出元素会把内容推出右边裁掉。 */
function fit(){
  var s=document.querySelector('.slide');
  s.style.position='fixed'; s.style.top='0'; s.style.left='0'; s.style.transformOrigin='top left';
  var sw=s.offsetWidth, sh=s.offsetHeight;
  var k=Math.min(window.innerWidth/sw, window.innerHeight/sh);
  var x=(window.innerWidth - sw*k)/2, y=(window.innerHeight - sh*k)/2;
  s.style.transform='translate('+x.toFixed(2)+'px,'+y.toFixed(2)+'px) scale('+k.toFixed(4)+')';
}
window.addEventListener('resize',fit);
window.addEventListener('load',fit);
fit();

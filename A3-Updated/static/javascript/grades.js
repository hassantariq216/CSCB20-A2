function expand(tabName) {
  if (document.getElementById(tabName).className === "expanded") {
    document.getElementById(tabName).className = "collapsed";
  } else {
    let i, x;
    x = document.getElementsByClassName("expanded");
    for (i = 0; i < x.length; i++) {
      x[i].className = "collapsed";
    }
    document.getElementById(tabName).className = "expanded";
  }
}

function popper(popOut) {
  let modal = document.getElementById(popOut);
  let span = document.getElementById(popOut + 'c');

  modal.style.display = "block";

  span.onclick = function() {
    modal.style.display = "none";
  };
}
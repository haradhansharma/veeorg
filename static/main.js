
if (document.querySelector('header')) {
    // Get the header element
    var header = document.querySelector('header');
    // Get the height of the header
    var headerHeight = header.offsetHeight;
}

//get the rem
var rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
var newPaddingTop = headerHeight + rem + 'px';

if (document.querySelector('main')) {
    // Get the content element
    var content = document.querySelector('main');
    // Set the padding of the content element
    content.style.paddingTop = newPaddingTop;
}


if (document.querySelector('#sidebarDiv')) {
    var content3 = document.querySelector('#sidebarDiv');
    content3.style.paddingTop = headerHeight + 10 + 'px';
}

if (document.querySelector('#sidebarDiv2')) {
    var content3 = document.querySelector('#sidebarDiv2');
    content3.style.paddingTop = headerHeight + 10 + 'px';
}

if (document.querySelector('.sidebarDiv3')) {
    var content3 = document.querySelector('.sidebarDiv3');
    content3.style.paddingTop = headerHeight + 'px';
}








if (document.querySelector('.topsection')){
    // Get the topsection element
    var topsection = document.querySelector('.topsection');
    // Get the height of the topsection
    var topsectionHeight = topsection.offsetHeight;
    console.log(topsectionHeight)

    var tptop = document.querySelector('.tp-top');
    var tpbottom = document.querySelector('.tp-bottom');
    if (tptop) {      
        tptop.style.minHeight  = topsectionHeight / 2 + 'px';
    }

    if (tpbottom) {      
        tpbottom.style.minHeight  = topsectionHeight / 2 + 'px';
    }
}







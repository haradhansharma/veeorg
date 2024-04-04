/*

  Main JavaScript File for Human Sun Folio Template

  Author: Haradhan Sharma
  Date: April 2, 2024
  Version: 1.0

  This is the main JavaScript file for your website. It controls the interactivity and functionality 
  of your web pages. 

  **Dependencies:**  MagicMouse JS, Vivus JS, OverlayScrollbar

*/
$(document).ready(function() {    
    // Print button 
    $('.printButton').on('click', function() {
      window.print(); 
    });
    // print button  

    // go back button      
    $('#goBackButton').click(function() {
        goBack();
      });
    // go back button


    // magic mouse settings start ===============>       
    var mm_options = {
        "outerStyle": "circle",
        "hoverEffect": "pointer-overlay",
        "hoverItemMove": false,
        "defaultCursor": false,
        "outerWidth": 40,
        "outerHeight": 40
    }; 

    //initiate magic ouse
    magicMouse(mm_options); 

    // altering default behacior of magic mouse 
    alterMagicMouse(); 
    
    // applyng magic mouse with different blend mode
    $('.specialeffect').each(function() {
        changeMouseSize($(this), mm_options);
    });  

    // applying magic mouse with pointer blur
    $('.specialeffectImage').each(function() {  
        changeMouseSize($(this), mm_options, "pointer-blur");        
    });
    

    // car effect with magic mouse
    $('.cardeffectEx').each(function() {
        setCardEffectMagicMouse($(this));
    });


    // calling windows loader. ust be after magic mouse
    callLoader();

    // magic mouse settings end ===========>
    

    // Vivus settings ============================>    
    // Call the function for each element ID
    initVivusAnimation('arrow_to_video', 200, 3000);
    initVivusAnimation('pegion', 200, 3000);        
    // Vivus settings ============================>  


    // Overlay JS configuration as per doc 
    var { 
        OverlayScrollbars, 
        ScrollbarsHidingPlugin, 
        SizeObserverPlugin, 
        ClickScrollPlugin  
    } = OverlayScrollbarsGlobal;

    // Initialize OverlayScrollbars for the body
    OverlayScrollbars(document.body, {});  


    // Initialize OverlayScrollbars for the #applyScrolbar element
    var applyScrollbarElement = document.querySelector('#applyScrolbar');
    if (applyScrollbarElement) {
        OverlayScrollbars(applyScrollbarElement, {
            overflow: {
                x: 'hidden',
                y: 'scroll'
            },
        });
    } else {
        console.error('Element with ID "applyScrolbar" not found.');
    }
    // end overlay scroll bar



    // got to top button
    $(window).scroll(function() {
    if ($(this).scrollTop() > 20) {
          $('#goToTopBtn').fadeIn();
        } else {
          $('#goToTopBtn').fadeOut();
        }
    });

    $('#goToTopBtn').click(function() {
        $('html, body').animate({
          scrollTop: 0
        }, 200);
    });
    // go to top button


    // glitbox gallery start. refer to the documentation of glitbox
    // glightbox defined in scripts.html   


    var lightbox1 = GLightbox({
        touchNavigation : true,
        loop : true,
        autoplayVideos : true,
        selector : '.glightbox1'
    });
    var lightbox2 = GLightbox({
        touchNavigation : true,
        loop : true,
        autoplayVideos : true,
        selector : '.glightbox2',
    });
    
    // glitbox gallery end    


    // skills marquee =============>
    // Call the function for each container with their respective direction
    setupMarquee('marqueeContainer', 'left');
    setupMarquee('marqueeContainer2', 'left');
    setupMarquee('marqueeContainer3', 'right'); 
    // skills marquee =============>


    // Explore me section icon animation start
    $(".explore-cards").each(function(){   
        // resetting to the default for background color
        $(this).on('mouseenter', function(){
            $(this).find('.bs-icon').addClass('end-0 bg-danger');
        });
        $(this).on('mouseleave', function(){
            $(this).find('.bs-icon').removeClass('end-0 bg-danger');
        });
    }); 
    // Explore me section icon animation end     

});

function changeMouseSize(eL, mm_options, hoverEffect = "pointer-overlay") {
    var specialeffect = $(eL);
    var specialeffectWidthHalf = specialeffect.width() / 2;
    var magicPointer = $('body #magicPointer');
    var magicMouseCursor  = $('body #magicMouseCursor');

    // Altering the original size based on eL
    specialeffect.on('mouseenter', function() {
        magicPointer.css({
            width: (specialeffectWidthHalf) + "px",
            height: (specialeffectWidthHalf) + "px"
        });
        magicMouseCursor.css({
            border: "none",
        });
        magicPointer.removeClass(mm_options.hoverEffect);
        magicPointer.addClass(hoverEffect);     

    });

    // Resetting default size and hover effect
    specialeffect.on('mouseleave', function() {
        magicPointer.css({
            width: "",
            height: ""
        });      
        magicMouseCursor.css({
            border: "",
        });
        magicPointer.removeClass(hoverEffect);   
        magicPointer.addClass(mm_options.hoverEffect);  
    });
}

// go back button
function goBack() {
  window.history.back();
}

// loader
function showLoader() {
    $('#main').addClass('hidden');
    $('#loader').removeClass('hidden');
    $('#loader .circle').removeClass('hidden');
}

function hideLoader() {
    $('#main').removeClass('hidden');
    $('#loader').addClass('hidden');
    $('#loader .circle').addClass('hidden');
}

function callLoader() {
    showLoader();
    if (document.readyState === 'complete') {
        hideLoader();
    } else {
        setTimeout(function() {
            hideLoader();
        }, 500);
    }
}
// Loader


function setupMarquee(containerId, direction) {
    const container = $('#' + containerId);
    const items = container.find('.scrolling-content');
    const containerWidth = container.width();

    let originalWidth = 0;
    items.each(function() {
        originalWidth += $(this).outerWidth();
    });

    let totalWidth = 0;

    if (direction === 'left') {
        while (totalWidth < containerWidth) {
            items.each(function() {
                const clone = $(this).clone(true);
                container.append(clone);
                totalWidth += clone.outerWidth();
            });
        }
    } else if (direction === 'right') {
        while (totalWidth < containerWidth) {
            items.each(function() {
                const clone = $(this).clone(true);
                container.prepend(clone);
                totalWidth += clone.outerWidth();
            });
        }
    }

    let scrollPosition = 0;

    function loopMarquee() {
        if (direction === 'left') {
            scrollPosition -= 0.5;
        } else if (direction === 'right') {
            scrollPosition += 0.5;
        }
        
        container.css('transform', `translateX(${scrollPosition}px)`);

        if (direction === 'left' && Math.abs(scrollPosition) >= originalWidth) {
            scrollPosition = 0;
            container.css('transform', `translateX(${scrollPosition}px)`);
        } else if (direction === 'right' && scrollPosition >= originalWidth) {
            scrollPosition = 0;
            container.css('transform', `translateX(${scrollPosition}px)`);
        }
        requestAnimationFrame(loopMarquee);
    }
    loopMarquee();
}

// Vivus SVG animation as per vivus js doc
function initVivusAnimation(elementId, duration, speed) {
    var element = $('#' + elementId);
    if (element.length > 0) {
        new Vivus(elementId, {
            type: 'delayed',
            duration: duration,
            animTimingFunction: Vivus.EASE
        }, function (myVivus) {
            setTimeout(function () {
                myVivus.play(myVivus.getStatus() === 'end' ? -1 : 1);
            }, speed);
        });
    }
}

function alterMagicMouse() {
    const mousePointerTrans = "background 0.5s, width 0.4s, height 0.4s, border-radius 0.4s";
    // altering default pointer
    $('body #magicPointer').css({
        transition : mousePointerTrans,       
        'z-index': '9999999',
    });  
}



// Ading card effect based on magic mouse
function setCardEffectMagicMouse(eL) {   
    var card = eL;
    var mouseHover = false;
    var mousePosition = { x: 0, y: 0 };
    var cardSize = { width: 0, height: 0 };
    var SCALE_X = 4;
    var SCALE_Y = 8;

    card.blur(function() {
        mouseHover = false;
    });

    card.focus(function() {
        mouseHover = true;
    });

    card.mousemove(function(e) {
        if (!mouseHover) return;
        var rect = card[0].getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        mousePosition = { x, y };
        cardSize = {
            width: card[0].offsetWidth || 0,
            height: card[0].offsetHeight || 0,
        };
        card.css({
            'transition': 'transform 0.4s ease', 
            'transform': 'perspective(1000px) rotateX(' + ((mousePosition.y / cardSize.height) * -(SCALE_Y * 2) + SCALE_Y) + 'deg) rotateY(' + ((mousePosition.x / cardSize.width) * (SCALE_X * 2) - SCALE_X) + 'deg) translateZ(10px)'
            });
    });

    card.mouseout(function() {
        mouseHover = false;
        card.css('transform', 'perspective(600px) rotateX(0deg) rotateY(0deg) translateZ(0px)');
    });

    card.mouseover(function() {
        mouseHover = true;
    });
} 

    

      














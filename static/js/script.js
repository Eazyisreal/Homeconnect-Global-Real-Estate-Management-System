// Get the grid container and control elements
const gridContainer = document.querySelector('.managed-properties-grid');
const leftArrow = document.querySelector('.controls img[alt="Arrow facing left"]');
const rightArrow = document.querySelector('.controls img[alt="Arrow facing right"]');

leftArrow.addEventListener('click', () => {
    const scrollPosition = gridContainer.scrollLeft;
    if (scrollPosition > 0) {
      gridContainer.scrollBy(-gridContainer.offsetWidth, 0);
    }
  });
  
  rightArrow.addEventListener('click', () => {
    const scrollPosition = gridContainer.scrollLeft;
    const maxScrollPosition = gridContainer.scrollWidth - gridContainer.offsetWidth;
    if (scrollPosition < maxScrollPosition) {
      gridContainer.scrollBy(gridContainer.offsetWidth, 0);
    }
  });

  const scrollers = document.querySelectorAll(".scroller");
  if (!window.matchMedia("(prefers-reduced-motion)").matches) {
    addAnimation();
  }
  
  function addAnimation() {
    scrollers.forEach((scroller) => {
      scroller.setAttribute("data-animated", true);
  
      const scrollerInner =  scroller.querySelector(".testimonial-wrapper");
      const scrollerContent = Array.from(scrollerInner.children);
  
      scrollerContent.forEach(item => {
          const duplicatedItem = item.cloneNode(true)
          duplicatedItem.setAttribute('aria-hidden', true);
          scrollerInner.appendChild(duplicatedItem);
      })
    });
  }
  
(() => {
  'use strict';
  const slides = JSON.parse(document.querySelector('#slides').textContent);
  const video = document.querySelector('#video');
  const cover = document.querySelector('#cover');
  const previous = document.querySelector('#previous');
  const next = document.querySelector('#next');
  const hint = document.querySelector('#play-hint');
  const error = document.querySelector('#media-error');
  const chapters = [...document.querySelectorAll('.chapter')];
  let current = -1;
  function fromHash() {
    const match = location.hash.match(/^#slide-(\d+)$/);
    return match ? Math.max(0, Math.min(19, Number(match[1]) - 1)) : 0;
  }
  function show(index, play = false, scroll = false) {
    index = Math.max(0, Math.min(slides.length - 1, index));
    if (index === current) {
      if (scroll) document.querySelector('#watch').scrollIntoView({block:'start'});
      return;
    }
    current = index;
    const slide = slides[index];
    video.pause();
    video.removeAttribute('src');
    video.load();
    error.hidden = true;
    video.hidden = index === 0;
    cover.hidden = index !== 0;
    if (index !== 0) {
      video.poster = slide.poster;
      video.src = slide.file;
      video.setAttribute('aria-label', `Slide ${index + 1}: ${slide.title}`);
      if (play) video.play().catch(() => {});
    }
    previous.disabled = index === 0;
    next.textContent = index === 0 ? 'Start watching →' : index === 19 ? 'Back to the cover ↺' : 'Next slide →';
    document.querySelector('#counter').textContent = `${String(index + 1).padStart(2,'0')} / 20`;
    document.querySelector('#slide-title').textContent = slide.title;
    hint.textContent = index === 0 ? 'Use Next or swipe to move through the night. Sound is part of the story.' : 'Tap ▶ to play with sound. Use Next when you’re ready for the next moment.';
    chapters.forEach((chapter,n) => {
      if (n === index) chapter.setAttribute('aria-current','true');
      else chapter.removeAttribute('aria-current');
    });
    history.replaceState(null,'',`#slide-${index + 1}`);
    if (scroll) document.querySelector('#watch').scrollIntoView({block:'start'});
  }
  previous.addEventListener('click', () => show(current - 1, true));
  next.addEventListener('click', () => show(current === 19 ? 0 : current + 1, true));
  chapters.forEach((chapter,n) => chapter.addEventListener('click', () => show(n,true,true)));
  document.addEventListener('keydown', e => {
    if (/INPUT|TEXTAREA|SELECT|VIDEO/.test(e.target.tagName) || e.altKey || e.metaKey || e.ctrlKey) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); show(current + 1,true); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(current - 1,true); }
  });
  let touch = null;
  const stage = document.querySelector('#stage');
  stage.addEventListener('touchstart', e => {
    const point = e.changedTouches[0], rect = stage.getBoundingClientRect();
    touch = point.clientY < rect.bottom - 70 ? {x:point.clientX,y:point.clientY} : null;
  },{passive:true});
  stage.addEventListener('touchend', e => {
    if (!touch) return;
    const dx=e.changedTouches[0].clientX-touch.x, dy=e.changedTouches[0].clientY-touch.y;
    if (Math.abs(dx)>65 && Math.abs(dx)>Math.abs(dy)*1.5) show(current+(dx<0?1:-1),true);
    touch=null;
  },{passive:true});
  video.addEventListener('error', () => { if (video.getAttribute('src')) error.hidden=false; });
  video.addEventListener('ended', () => {hint.textContent=current===19?'A night to remember. Thank you for watching.':'That’s this moment. Tap Next slide to keep watching.';});
  video.addEventListener('play', () => {hint.textContent='Original concert sound. You can pause, replay, or move to the next slide.';});
  document.querySelector('#retry').addEventListener('click', () => {error.hidden=true;video.load();video.play().catch(()=>{});});
  window.addEventListener('hashchange', () => show(fromHash()));
  show(fromHash());
})();

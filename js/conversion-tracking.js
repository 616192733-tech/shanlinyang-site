(function(){
  function label(el){
    return el.getAttribute('data-track') || el.textContent.trim().slice(0,80) || el.href;
  }
  function track(name, data){
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({event:name}, data || {}));
    if (window.gtag) window.gtag('event', name, data || {});
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href]');
    if(!a) return;
    var href = a.getAttribute('href') || '';
    if(href.indexOf('wa.me/') !== -1 || href.indexOf('whatsapp') !== -1){
      track('whatsapp_click', {link_text: label(a), page_path: location.pathname, href: href});
    }
    if(href.indexOf('/contact.html') === 0 || href.indexOf('mailto:') === 0){
      track('inquiry_click', {link_text: label(a), page_path: location.pathname, href: href});
    }
  }, {passive:true});
})();

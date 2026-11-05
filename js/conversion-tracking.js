(function(){
  var storageKey = 'sly_acquisition_v1';

  function safeHost(value){
    try { return value ? new URL(value).hostname.toLowerCase().replace(/^www\./, '') : ''; }
    catch (e) { return ''; }
  }

  function detectSource(params, referrerHost){
    var tagged = (params.get('utm_source') || '').toLowerCase();
    var value = tagged || referrerHost;
    if (value.indexOf('chatgpt') !== -1 || value.indexOf('openai') !== -1) return 'ChatGPT';
    if (value.indexOf('perplexity') !== -1) return 'Perplexity';
    if (value.indexOf('gemini') !== -1 || value.indexOf('bard.google') !== -1) return 'Gemini';
    if (value.indexOf('claude') !== -1 || value.indexOf('anthropic') !== -1) return 'Claude';
    if (value.indexOf('copilot') !== -1) return 'Microsoft Copilot';
    if (tagged) return tagged;
    if (referrerHost) return referrerHost;
    return 'direct';
  }

  function getAcquisition(){
    var saved = null;
    try { saved = JSON.parse(localStorage.getItem(storageKey) || 'null'); } catch (e) {}
    if (saved && saved.source) return saved;

    var params = new URLSearchParams(location.search);
    var referrerHost = safeHost(document.referrer);
    var record = {
      source: detectSource(params, referrerHost),
      referrer_hostname: referrerHost || 'direct',
      first_landing_path: location.pathname,
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
      captured_at: new Date().toISOString()
    };
    try { localStorage.setItem(storageKey, JSON.stringify(record)); } catch (e) {}
    return record;
  }

  var acquisition = getAcquisition();
  window.shanlinyangAcquisition = acquisition;

  var acquisitionFields = {
    'acquisition-source': acquisition.source,
    'first-referrer': acquisition.referrer_hostname,
    'first-landing-page': acquisition.first_landing_path,
    'utm-source': acquisition.utm_source,
    'utm-medium': acquisition.utm_medium,
    'utm-campaign': acquisition.utm_campaign
  };
  Object.keys(acquisitionFields).forEach(function(id){
    var input = document.getElementById(id);
    if (input) input.value = acquisitionFields[id] || '';
  });

  function label(el){
    return el.getAttribute('data-track') || el.textContent.trim().slice(0,80) || el.href;
  }
  function track(name, data){
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({
      event: name,
      acquisition_source: acquisition.source,
      first_referrer: acquisition.referrer_hostname
    }, data || {}));
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

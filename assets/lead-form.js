/* Gridlas shared lead-capture. Attach to any
   <form class="lead-form" data-source="..." data-pdf="path">
   containing an <input type="email">. Posts to Klaviyo (kmail-lists.com),
   downloads the sample PDF on success, and shows a toast (self-created). */
(function () {
  var LIST = 'Um8YCH';
  function toast(msg, ok) {
    var t = document.getElementById('gl-toast');
    if (!t) { t = document.createElement('div'); t.id = 'gl-toast'; t.className = 'gl-toast'; document.body.appendChild(t); }
    t.textContent = msg;
    t.style.background = ok ? 'var(--cyan)' : '#FF7A3C';
    t.style.color = '#06131A';
    t.style.display = 'block';
    setTimeout(function () { t.style.display = 'none'; }, 4500);
  }
  function grab(pdf) {
    if (!pdf) return;
    try { var a = document.createElement('a'); a.href = pdf; a.download = ''; document.body.appendChild(a); a.click(); a.remove(); } catch (e) {}
  }
  function wire(form) {
    var src = form.getAttribute('data-source') || 'gridlas-subpage';
    var pdf = form.getAttribute('data-pdf') || '';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var inp = form.querySelector('input[type=email]');
      var email = (inp && inp.value || '').trim();
      if (!email) return;
      var body = new URLSearchParams({ g: LIST, email: email, '$source': src });
      fetch('https://manage.kmail-lists.com/ajax/subscriptions/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body
      })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d && d.success) { grab(pdf); form.reset(); toast('✓ Check your inbox — summary on the way.', true); }
          else { toast((d && d.errors && d.errors[0]) || 'Hmm, try again in a moment.', false); }
        })
        .catch(function () { grab(pdf); toast('✓ Summary on the way.', true); });
    });
  }
  function init() { Array.prototype.forEach.call(document.querySelectorAll('form.lead-form'), wire); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

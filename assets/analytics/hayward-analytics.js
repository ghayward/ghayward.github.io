/* Hayward Data Science Website only. This is a public ingestion key, not a secret. */
(function () {
  'use strict';

  var pages = { '/': 'home', '/index.html': 'home', '/projects.html': 'projects', '/resume.html': 'resume' };
  var page = pages[window.location.pathname];
  if (!page || !/^https?:$/.test(window.location.protocol) ||
      !/^(www\.)?haywarddatascience\.com$/.test(window.location.hostname)) return;

  var links = {
    '/soundrecipe-app': ['Portfolio Item Clicked', 'soundrecipe'],
    '/setlist2playlist-app': ['Portfolio Item Clicked', 'setlist2playlist'],
    '/youtube-tracking-app': ['Portfolio Item Clicked', 'youtube_tracking'],
    '/data-projects': ['Portfolio Item Clicked', 'data_projects'],
    '/get-help': ['Professional Intent Clicked', 'consulting'],
    '/cv': ['Professional Intent Clicked', 'resume'],
    '/teach-mentor-rec': ['Professional Intent Clicked', 'mentoring'],
    '/mentor': ['Professional Intent Clicked', 'mentoring'],
    '/contact': ['Professional Intent Clicked', 'contact'],
    '/hayward-github': ['Professional Intent Clicked', 'github'],
    '/hayward-linkedin': ['Professional Intent Clicked', 'linkedin'],
    '/data-science-project-1-ml-plus-supervised-pca-segmentation': ['Portfolio Item Clicked', 'project_01'],
    '/data-science-project-2-time-series-arima-prophet-plus-classification': ['Portfolio Item Clicked', 'project_02'],
    '/data-science-project-3-ab-testing-inference-k-means-clustering': ['Portfolio Item Clicked', 'project_03'],
    '/data-science-project-4-predict-insurance-losses': ['Portfolio Item Clicked', 'project_04'],
    '/data-science-project-5-spotify-playlist-analysis-success': ['Portfolio Item Clicked', 'project_05'],
    '/data-science-project-6-increasing-tipping-rates': ['Portfolio Item Clicked', 'project_06'],
    '/data-science-project-7-news-content-consumption': ['Portfolio Item Clicked', 'project_07'],
    '/data-science-project-8-sql-python-matplotlib': ['Portfolio Item Clicked', 'project_08'],
    '/data-science-project-9-polling-statistical-inference': ['Portfolio Item Clicked', 'project_09'],
    '/data-science-project-10-hayward-weightloss-streak-analysis': ['Portfolio Item Clicked', 'project_10']
  };
  var client;
  var queue = [];
  var failed = false;

  function ignoreFailure(result) {
    if (result && result.promise) result.promise.catch(function () {});
  }

  function track(name, item, placement) {
    try {
      if (failed) return;
      var properties = {
        page: page,
        page_path: page === 'home' ? '/' : window.location.pathname,
        environment: 'production'
      };
      if (item) properties.item_id = item;
      if (placement) properties.placement = placement;
      if (client) ignoreFailure(client.track(name, properties));
      else if (queue.length < 30) queue.push([name, properties]);
    } catch (error) { /* Analytics must never interfere with the page. */ }
  }

  function onClick(event) {
    try {
      if (event.type === 'auxclick' && event.button !== 1) return;
      var anchor = event.target.closest('a[href]');
      if (!anchor) return;
      var url = new URL(anchor.href);
      if (url.hostname !== 'go.haywarddatascience.com') return;
      var link = links[url.pathname];
      if (link) track(link[0], link[1], anchor.closest('nav') ? 'navigation' : 'project_list');
    } catch (error) { /* Leave normal navigation alone, including when blocked. */ }
  }

  function stop() {
    failed = true;
    queue = [];
    client = null;
  }

  try {
    document.addEventListener('click', onClick);
    document.addEventListener('auxclick', onClick);
    track('Page Viewed');
    var sdk = document.createElement('script');
    sdk.async = true;
    sdk.src = 'https://cdn.amplitude.com/libs/analytics-browser-2.47.0-min.js.gz';
    sdk.onerror = stop;
    sdk.onload = function () {
      try {
        var instance = window.amplitude.createInstance();
        instance.init('5013e0649d3c621a041cdda3cec17b91', undefined, {
          serverZone: 'US',
          autocapture: false,
          fetchRemoteConfig: false,
          trackingOptions: { ipAddress: false },
          cookieOptions: { domain: window.location.hostname },
          flushQueueSize: 1
        }).promise.then(function () {
          client = instance;
          queue.forEach(function (event) {
            ignoreFailure(client.track(event[0], event[1]));
          });
          queue = [];
        }).catch(stop);
      } catch (error) { stop(); }
    };
    document.head.appendChild(sdk);
  } catch (error) { stop(); }
}());

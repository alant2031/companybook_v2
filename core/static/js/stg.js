document.addEventListener(
	'DOMContentLoaded',
	function () {
		// Telegram
		let tg_url = encodeURIComponent(window.location.href); //url
		let tg_title = encodeURIComponent(document.title); //título
		let tg_link = `https://t.me/share/url?url=${tg_url}&text=${tg_title}`;
		document.getElementById('telegram-share-btt').href = tg_link;
	},
	false,
);

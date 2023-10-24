document.addEventListener(
	'DOMContentLoaded',
	function () {
		// Whatsapp
		let content = encodeURIComponent(
			document.title + ' ' + window.location.href,
		);
		document.getElementById('whatsapp-share-btt').href =
			'https://api.whatsapp.com/send?text=' + content;
	},
	false,
);

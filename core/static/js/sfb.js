document.addEventListener(
	'DOMContentLoaded',
	function () {
		//Facebook
		document.getElementById('facebook-share-btt').href =
			'https://www.facebook.com/sharer/sharer.php?u=' +
			encodeURIComponent(window.location.href);
	},
	false,
);

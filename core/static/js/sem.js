const email_share = function () {
	// Email
	let email_url = window.location.href;
	let email_title = encodeURIComponent(document.title);
	let mailToLink = 'mailto:?subject=' + email_title;

	let desc = document.querySelector("meta[name='description']");
	desc = !!desc ? desc.getAttribute('content') : null;

	if (!desc) {
		desc = document.querySelector("meta[property='og:description']");
		desc = !!desc ? desc.getAttribute('content') : null;
	}
	let body = !!desc ? desc + ' ' + email_url : email_url;
	mailToLink = mailToLink + '&body=' + encodeURIComponent(body);
	document.getElementById('mail-share-btt').href = mailToLink;
};

document.addEventListener('DOMContentLoaded', () => {}, false);

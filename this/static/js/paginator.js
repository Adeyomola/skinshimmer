const pageNumbers = document.querySelectorAll(".pageNumbers");
const href = decodeURI(window.location.pathname + window.location.search);

pageNumbers.forEach((page) => {
  if (href === page.getAttribute("href")) page.className += " active";
  else if (href === decodeURI(window.location.pathname))
    pageNumbers[0].className += " active";
});

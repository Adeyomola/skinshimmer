const pageNumbers = document.querySelectorAll(".pageNumbers");
const href = decodeURI(window.location.pathname + window.location.search);
console.log(href);

pageNumbers.forEach((page) => {
  console.log(page.getAttribute("href"));
  if (href === page.getAttribute("href")) page.className += " active";
  else if (href === window.location.pathname)
    pageNumbers[0].className += " active";
});

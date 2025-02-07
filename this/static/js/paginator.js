const pageNumbers = document.querySelectorAll(".pageNumbers");
const href = window.location.pathname + window.location.search;
console.log(href);
console.log(page.getAttribute("href"));

pageNumbers.forEach((page) => {
  if (href === page.getAttribute("href")) page.className += " active";
  else if (href === window.location.pathname)
    pageNumbers[0].className += " active";
});

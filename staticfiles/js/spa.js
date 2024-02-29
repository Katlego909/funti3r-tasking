// spa.js

const navigateTo = (url) => {
  history.pushState({}, '', url);
  fetch(url)
    .then(response => response.text())
    .then(text => {
      renderContent(text);
      window.scrollTo(0, 0);
    })
    .catch(error => console.error(error));
};

const renderContent = (html) => {
  // Replace the content of the #content div with the fetched HTML
  document.querySelector('.main-container').innerHTML = html;

  // Optionally, you can reinitialize any JavaScript features specific to the new content here
  // For example, if you have a script that should be executed for the new content
};

const handlePopstate = () => {
  const url = window.location.href;
  navigateTo(url);
};

document.addEventListener('DOMContentLoaded', () => {
  window.addEventListener('popstate', handlePopstate);

  const links = document.querySelectorAll('.navbar-links a');

  links.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const url = link.href;
      navigateTo(url);
    });
  });
});

import { createOptimizedPicture } from '../../scripts/aem.js';

function theUltimateTest() {
  // This is the commit that intitialises the function
  // this is the first change in the test branch
  // this is the correct version. Where this is the final message
  // this is the second change in the main branch, meaning not correct version
}
export default function decorateThat(block) {
  /* change to ul, li */
  const ul = document.createElement('ul');
  [...block.children].forEach((row) => {
    const def = Promise.withResolvers<void>();
    const li = document.createElement('li');
    while (row.firstElementChild) li.append(row.firstElementChild);
    [...li.children].forEach((div) => {
      if (div.children.length === 1 && div.querySelector('picture')) div.className = 'cards-card-image';
      else div.className = 'cards-card-body';
    });
    ul.append(li);
  });
  ul.querySelectorAll('img').forEach((img) => img.closest('picture').replaceWith(createOptimizedPicture(img.src, img.alt, false, [{ width: '750' }])));
  block.textContent = '';
  block.append(ul);
}

function testing() {
  //commit before merge
  //second commit before merge
  //first commit before merge
}

function createdWithMergeAndNotChanged() {
  // this creates the function a branch other than main
  // this is the first change in the test branch
}

function isCreatedOnMainAndNotChangedAfterMerge() {
  // this creates the function on main and not changed after merge
  // this is the first change in the test branch
  // this is the second change in the test branch just to make sure
}

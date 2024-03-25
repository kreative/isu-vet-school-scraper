const axios = require("axios");
const cheerio = require("cheerio");

const alphabet = [
  "a",
  "b",
  "c",
  "d",
  "e",
  "f",
  "g",
  "h",
  "i",
  "j",
  "k",
  "l",
  "m",
  "n",
  "o",
  "p",
  "q",
  "r",
  "s",
  "t",
  "u",
  "v",
  "w",
  "x",
  "y",
  "z",
];

const getUserContent = async (path) => {
  const url = `https://vetmed.iastate.edu${path}`;
  const response = await axios.get(url);
  const $ = cheerio.load(response.data);
  const professionalTitle = $(
    ".field-name-field-professional-title .field-item",
  )
    .text()
    .trim();
  const degrees = $(".field-name-field-degrees .field-item").text().trim();

  return {
    professionalTitle,
    degrees,
  };
};

const getDirectoryPage = async (letter) => {
  const url = `https://vetmed.iastate.edu/directory/${letter}`;
  const response = await axios.get(url);
  const $ = cheerio.load(response.data);
  const directory = [];
  const tbody = $("tbody");

  if (tbody.length) {
    tbody.find("tr").each((index, element) => {
      const lastNameCell = $(element).find(".views-field-field-c-last-name");
      const lastName = lastNameCell.text().trim();
      const anchor = lastNameCell.find("a");
      const href = anchor.attr("href");
      const firstNameCell = $(element).find(".views-field-field-c-first-name");
      const firstName = firstNameCell.text().trim();
      const departmentCell = $(element).find(".views-field-field-department");
      const department = departmentCell.text().trim();
      const phoneNumberCell = $(element).find(".views-field-field-c-phone");
      const phoneNumber = phoneNumberCell.text().trim();
      const emailCell = $(element).find(".views-field-field-c-email");
      const email = emailCell.text().trim();

      directory.push({
        lastName,
        firstName,
        department,
        phoneNumber,
        email,
        href,
      });
    });
  } else {
    console.log("No tbody found on the page.");
  }

  return directory;
};

const run = async () => {
  console.log("ISU Vet School Scraper Starting...");

  const directory = await getDirectoryPage("a");

  console.log(directory);
};

run();

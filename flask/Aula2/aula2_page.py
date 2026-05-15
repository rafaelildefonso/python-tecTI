from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta http-equiv="X-UA-Compatible" content="IE=edge" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>3D Portfolio Website | Rafael</title>
      <!-- box icons -->
      <style>
      @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap");
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    text-decoration: none;
    border: none;
    outline: none;
    font-family: "Poppins", sans-serif;
  }
  
  :root {
    --bg-color: #081b29;
    --main-color: #00abf0;
    --text-color: #333;
    --second-text-color: #555;
    --white-color: #fff;
    --cover-color: linear-gradient(45deg, #00abf0, #006e9a);
    --pages-color: linear-gradient(90deg, #fff, #ddd);
    --border: 0.125rem solid #00abf0;
    --box-shadow: 0 0 0.6rem rgba(0, 0, 0, 0.2);
  }
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: var(--bg-color);
    color: var(--text-color);
    overflow: hidden;
  }
  .wrapper {
    position: relative;
    width: 66rem;
    height: 45rem;
    padding: 2rem;
    perspective: 250rem;
    animation: show-animate 2s forwards;
  }
  
  @keyframes show-animate {
    0%,
    30% {
      opacity: 0;
      transform: rotate(-20deg);
    }
    100% {
      opacity: 1;
      transform: rotate(0deg);
    }
  }
  
  .cover {
    position: absolute;
    top: 0;
    left: 0;
    width: 50%;
    height: 100%;
    background: var(--cover-color);
    box-shadow: var(--box-shadow);
    border-top-left-radius: 0.6rem;
    border-bottom-left-radius: 0.6rem;
    transform-origin: right;
  }
  .cover.cover-left {
    z-index: -1;
  }
  .cover.cover-right {
    z-index: 100;
    transition: transform 1s cubic-bezier(0.645, 0.045, 0.355, 1);
  }
  .cover.cover-right.turn {
    transform: rotateY(180deg);
  }
  
  .book {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    perspective: 250rem;
  }
  .book .book-page {
    position: absolute;
    width: 50%;
    height: 100%;
    background: var(--pages-color);
    box-shadow: 0 0 0.6rem rgba(0, 0, 0, 0.1);
    display: flex;
    padding: 2rem;
  }
  .book-page.page-left {
    box-shadow: -0.6rem 0.6rem 0.6rem rgba(0, 0, 0, 0.1);
  }
  .profile-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .profile-page img {
    max-width: 180px;
    border-radius: 50%;
    border: 0.25rem solid var(--main-color);
    margin-bottom: 0.8rem;
  }
  .profile-page h1 {
    font-size: 2.7rem;
    line-height: 1;
  }
  .profile-page h3 {
    font-size: 1.5rem;
    color: var(--main-color);
  }
  .profile-page .social-media {
    margin: 0.6rem 0 0.8rem;
  }
  .profile-page .social-media a {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;
    background: transparent;
    border: var(--border);
    border-radius: 50%;
    font-size: 1.3rem;
    color: var(--main-color);
    margin: 0 0.2rem;
    transition: 0.5s;
  }
  .profile-page .social-media a:hover {
    background: var(--main-color);
    color: var(--white-color);
  }
  .profile-page p {
    text-align: justify;
  }
  .profile-page .btn-box {
    margin-top: 1.2rem;
  }
  
  .btn {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 9.5rem;
    height: 3rem;
    background: var(--main-color);
    border: var(--border);
    border-radius: 0.3rem;
    font-size: 1rem;
    color: var(--white-color);
    font-weight: 500;
    margin: 0 1rem;
    transition: 0.5s;
  }
  .btn:hover {
    background: transparent;
    color: var(--main-color);
  }
  .btn-box .btn:nth-child(2) {
    background: transparent;
    color: var(--main-color);
  }
  .btn-box .btn:nth-child(2):hover {
    background: var(--main-color);
    color: var(--white-color);
  }
  .book-page.page-right {
    position: absolute;
    right: 0;
    transform-style: preserve-3d;
    transform-origin: left;
    /* this is where we turn the pages as book */
    transition: transform 1s cubic-bezier(0.645, 0.045, 0.355, 1);
  }
  .book-page.page-right.turn {
    transform: rotateY(-180deg);
  }
  .book-page .page-front,
  .book-page .page-back {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--pages-color);
    padding: 1.5rem 2rem;
  }
  .book-page .page-front {
    transform: rotateY(0deg) translateZ(1px);
  }
  .book-page .page-back {
    transform: rotateY(180deg) translateZ(1px);
  }
  .title {
    text-align: center;
    margin-bottom: 1rem;
  }
  .workeduc-box {
    border-left: var(--border);
  }
  .workeduc-box .workeduc-content {
    position: relative;
  
    padding-left: 1.6rem;
    margin-bottom: 1.2rem;
  }
  .workeduc-box .workeduc-content:before {
    content: "";
    position: absolute;
    top: 0;
    left: -0.65rem;
    width: 1.2rem;
    height: 1.2rem;
    background: var(--main-color);
    border-radius: 50%;
  }
  .workeduc-content .year {
    color: var(--main-color);
  }
  .workeduc-content .year i {
    margin-right: 0.4rem;
  }
  .number-page {
    position: absolute;
    bottom: 1.2rem;
    left: 50%;
    transform: translateX(-50%);
  }
  .nextprev-btn {
    position: absolute;
    bottom: 0.9rem;
    right: 1.5rem;
    width: 2rem;
    height: 2rem;
  
    cursor: pointer;
    font-size: 2rem;
    color: var(--second-text-color);
    display: inline-flex;
    justify-content: center;
    align-items: center;
    transition: 0.5s;
  }
  .nextprev-btn:hover {
    color: var(--main-color);
  }
  .nextprev-btn.back {
    left: 1.5rem;
  }
  .services-box {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
  }
  .services-box .services-content {
    flex: 1 1 10rem;
    border: var(--border);
    border-radius: 0.5rem;
    text-align: center;
    padding: 0.8rem 0.5rem 1.1rem;
    transition: 0.3s ease;
  }
  .services-box .services-content:hover {
    box-shadow: var(--box-shadow);
  }
  
  .services-content i {
    font-size: 2.5rem;
    color: var(--main-color);
  }
  .services-content h3 {
    font-size: 1.1rem;
  }
  .services-content p {
    margin: 0.2rem 0 0.8rem;
  }
  .services-content .btn {
    width: 8rem;
    height: 2.5rem;
  }
  .skills-box {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
  }
  .skills-box .skills-content {
    flex: 1 1 20rem;
  }
  .skills-content h3 {
    font-size: 1.3rem;
    line-height: 1;
    margin-bottom: 0.6rem;
  }
  .skills-content .content {
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
  }
  .skills-content .content span {
    display: inline-flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 6rem;
    height: 5rem;
    border: var(--border);
    border-radius: 0.3rem;
    font-weight: 600;
    transition: 0.3s ease;
  }
  .skills-content .content span:hover {
    box-shadow: var(--box-shadow);
  }
  
  .skills-content .content span i {
    font-size: 3rem;
    color: var(--main-color);
  }
  .portfolio-box .img-box {
    display: flex;
    width: 100%;
    height: 15rem;
  
    border: var(--border);
    border-radius: 0.5rem;
    overflow: hidden;
  }
  .portfolio-box .img-box img {
    width: 100%;
    object-fit: cover;
    transition: 0.5s ease;
  }
  .portfolio-box .img-box:hover img {
    transform: scale(1.1);
  }
  .portfolio-box .info-box {
    margin: 1rem 0 1.5rem;
  }
  .portfolio-box .info-box .info-title {
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .portfolio-box .info-box .info-title h3 {
    font-size: 1.3rem;
  }
  .portfolio-box .info-box .info-title a {
    display: flex;
    align-items: center;
    color: var(--main-color);
  }
  .portfolio-box .info-box .info-title a i {
    margin-left: 0.3rem;
  }
  .portfolio-box .info-box p:nth-of-type(1) {
    font-weight: 600;
  }
  .portfolio-box .btn-box {
    display: flex;
    justify-content: center;
  }
  .portfolio-box .btn-box .btn {
    margin: 0 1.15rem;
  }
  .contact-box {
    text-align: center;
  }
  .contact-box .field {
    width: 100%;
    background: transparent;
    border: var(--border);
    border-radius: 0.3rem;
    padding: 0.8rem;
    margin-bottom: 1.5rem;
    font-size: 1rem;
    color: var(--second-text-color);
  }
  .contact-box .field::placeholder {
    color: var(--text-color);
  }
  .contact-box textarea {
    height: 15rem;
    resize: none;
  }
  .contact-box .btn {
    cursor: pointer;
  }
  .back-profile {
    position: absolute;
    bottom: 1.2rem;
    right: 2rem;
    width: 2rem;
    height: 2rem;
    background: transparent;
    border: var(--border);
    border-radius: 0.3rem;
    font-size: 1.1rem;
    color: var(--main-color);
    display: inline-flex;
    justify-content: center;
    align-items: center;
    transition: 0.5s;
  }
  .back-profile:hover {
    background: var(--main-color);
    color: var(--white-color);
  }
  .back-profile p {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%) scale(0.5);
    font-size: 1rem;
    color: var(--main-color);
    opacity: 0;
    transition: 0.5s;
  }
  .back-profile:hover p {
    opacity: 1;
    transform: translateX(-50%) scale(1);
    top: -1.8rem;
  }
  
  /* Responsive */
  @media screen and (max-width: 1024px) {
    .wrapper {
      width: 60rem;
      height: 40rem;
    }
  }
      </style>
    </head>
  
    <body>
      <div class="wrapper">
        <div class="cover cover-left"></div>
        <div class="cover cover-right"></div>
        <div class="book">
          <!-- profile page -->
          <div class="book-page page-left">
            <div class="profile-page">
              <img src="https://avatars.githubusercontent.com/u/159785876?v=4" alt="" />
              <h1>Rafael lldefonso</h1>
              <h3>Web Developer</h3>
              <div class="social-media">
                <a href="#"><i class="bx bxl-facebook"></i></a>
                <a href="#"><i class="bx bxl-twitter"></i></a>
                <a href="#"><i class="bx bxl-linkedin"></i></a>
                <a href="#"><i class="bx bxl-instagram-alt"></i></a>
              </div>
              <p>
                Hi, I am Rafael lldefonso. I am a web developer. Lorem ipsum dolor sit
                amet consectetur adipisicing elit. Fuga velit consequuntur vitae
                ea dignissimos voluptate odio labore, sed ducimus cumque nemo
                similique animi fugiat veritatis a laboriosam deserunt minus
                temporibus.
              </p>
              <div class="btn-box">
                <a href="#" class="btn">Download CV</a>
                <a href="#" class="btn contact-me">Contact Me</a>
              </div>
            </div>
          </div>
  
          <!-- page 1 & 2 -->
          <div class="book-page page-right turn" id="turn-1">
            <!-- page 1 (work experience) -->
            <div class="page-front">
              <h1 class="title">Work Experience</h1>
              <div class="workeduc-box">
                <div class="workeduc-content">
                  <span class="year"
                    ><i class="bx bx-calendar"></i>2020 - 2021</span
                  >
                  <h3>Master Degree - University</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga
                    velit consequuntur vitae ea dignissimos voluptate odio labore.
                  </p>
                </div>
                <div class="workeduc-content">
                  <span class="year"
                    ><i class="bx bx-calendar"></i>2021 - 2022</span
                  >
                  <h3>Master Degree - University</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga
                    velit consequuntur vitae ea dignissimos voluptate odio labore.
                  </p>
                </div>
                <div class="workeduc-content">
                  <span class="year"
                    ><i class="bx bx-calendar"></i>2022 - 2024</span
                  >
                  <h3>Master Degree - University</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga
                    velit consequuntur vitae ea dignissimos voluptate odio labore.
                  </p>
                </div>
              </div>
              <span class="number-page">1</span>
              <!-- next button -->
              <span class="nextprev-btn" data-page="turn-1"
                ><i class="bx bx-chevron-right"></i
              ></span>
            </div>
  
            <!-- page 2 (education) -->
            <div class="page-back">
              <h1 class="title">Education</h1>
  
              <div class="workeduc-box">
                <div class="workeduc-content">
                  <span class="year"
                    ><i class="bx bx-calendar"></i>2017 - 2018</span
                  >
                  <h3>Master Degree - University</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga
                    velit consequuntur vitae ea dignissimos voluptate odio labore.
                  </p>
                </div>
                <div class="workeduc-content">
                  <span class="year"
                    ><i class="bx bx-calendar"></i>2018 - 2019</span
                  >
                  <h3>Master Degree - University</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga
                    velit consequuntur vitae ea dignissimos voluptate odio labore.
                  </p>
                </div>
                <div class="workeduc-content">
                  <span class="year"
                    ><i class="bx bx-calendar"></i>2019 - 2020</span
                  >
                  <h3>Master Degree - University</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga
                    velit consequuntur vitae ea dignissimos voluptate odio labore.
                  </p>
                </div>
              </div>
  
              <span class="number-page">2</span>
              <!-- prev button -->
              <span class="nextprev-btn back" data-page="turn-1"
                ><i class="bx bx-chevron-left"></i
              ></span>
            </div>
          </div>
  
          <!-- page 3 & 4 -->
          <div class="book-page page-right turn" id="turn-2">
            <!-- page 3 (my services) -->
            <div class="page-front">
              <h1 class="title">My Services</h1>
              <div class="services-box">
                <div class="services-content">
                  <i class="bx bx-code-alt"></i>
                  <h3>Web Development</h3>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit.</p>
                  <a href="#" class="btn">Read More</a>
                </div>
                <div class="services-content">
                  <i class="bx bxs-paint"></i>
                  <h3>Creative Design</h3>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit.</p>
                  <a href="#" class="btn">Read More</a>
                </div>
                <div class="services-content">
                  <i class="bx bx-bar-chart-alt"></i>
                  <h3>Digital Marketing</h3>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit.</p>
                  <a href="#" class="btn">Read More</a>
                </div>
                <div class="services-content">
                  <i class="bx bx-search"></i>
                  <h3>SEO</h3>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit.</p>
                  <a href="#" class="btn">Read More</a>
                </div>
              </div>
              <span class="number-page">3</span>
              <!-- next button -->
              <span class="nextprev-btn" data-page="turn-2"
                ><i class="bx bx-chevron-right"></i
              ></span>
            </div>
  
            <!-- page 4 (my skills) -->
            <div class="page-back">
              <h1 class="title">My Skills</h1>
              <div class="skills-box">
                <div class="skills-content">
                  <h3>Front-End</h3>
                  <div class="content">
                    <span><i class="bx bxl-html5"></i>HTML</span>
                    <span><i class="bx bxl-css3"></i>CSS</span>
                    <span><i class="bx bxl-javascript"></i>JS</span>
                    <span><i class="bx bxl-react"></i>React</span>
                    <span><i class="bx bxs-terminal"></i>Next.js</span>
                    <span><i class="bx bxl-bootstrap"></i>Bootstrap</span>
                    <span><i class="bx bxl-tailwind-css"></i>Tailwind</span>
                  </div>
                </div>
                <div class="skills-content">
                  <h3>Back-End</h3>
                  <div class="content">
                    <span><i class="bx bxl-php"></i>PHP</span>
                    <span><i class="bx bxl-nodejs"></i>Node</span>
                    <span><i class="bx bx-terminal"></i>MySQL</span>
                    <span><i class="bx bxl-python"></i>Python</span>
                  </div>
                </div>
                <div class="skills-content">
                  <h3>UI/UX design</h3>
                  <div class="content">
                    <span><i class="bx bxl-figma"></i>Figma</span>
                  </div>
                </div>
              </div>
              <span class="number-page">4</span>
              <!-- prev button -->
              <span class="nextprev-btn back" data-page="turn-2"
                ><i class="bx bx-chevron-left"></i
              ></span>
            </div>
          </div>
          <!-- page 5 & 6 -->
          <div class="book-page page-right turn" id="turn-3">
            <!-- page 5 (latest project or my portfolio) -->
            <div class="page-front">
              <h1 class="title">Latest Project</h1>
              <div class="portfolio-box">
                <div class="img-box">
                  <img src="https://portfolio-rafaelildefonso.vercel.app/images/projects/shelfai.png" alt="" />
                </div>
                <div class="info-box">
                  <div class="info-title">
                    <h3>Project Name</h3>
                    <a href="#"
                      >Live Preview<i class="bx bx-link-external"></i
                    ></a>
                  </div>
                  <p>Tech Used</p>
                  <p>
                    Lorem, ipsum dolor sit amet consectetur adipisicing elit. A
                    saepe ipsam earum nulla dicta inventore ipsum, placeat,
                    itaque, sint.
                  </p>
                </div>
                <div class="btn-box">
                  <a href="#" class="btn">Source Code</a>
                  <a href="#" class="btn">More Projects</a>
                </div>
              </div>
              <span class="number-page">5</span>
              <!-- next button -->
              <span class="nextprev-btn" data-page="turn-3"
                ><i class="bx bx-chevron-right"></i
              ></span>
            </div>
            <!-- page 6 (contact me) -->
            <div class="page-back">
              <h1 class="title">Contact Me!</h1>
              <div class="contact-box">
                <form action="#">
                  <input
                    type="text"
                    class="field"
                    placeholder="Full Name"
                    required
                  />
                  <input
                    type="email"
                    class="field"
                    placeholder="Email Address"
                    required
                  />
                  <textarea
                    name=""
                    id=""
                    cols="30"
                    rows="10"
                    class="field"
                    placeholder="Your Message"
                    required
                  ></textarea>
                  <input type="submit" class="btn" value="Send Message" />
                </form>
              </div>
  
              <span class="number-page">6</span>
              <!-- prev button -->
              <span class="nextprev-btn back" data-page="turn-3"
                ><i class="bx bx-chevron-left"></i
              ></span>
              <a href="#" class="back-profile">
                <p>Profile</p>
                <i class="bx bxs-user"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
  
      <!-- what I used : HTML, CSS, JS, Boxicons,  -->
  
      <script>
      //turn pages when click next or prev button
  const pageTurnBtn = document.querySelectorAll(".nextprev-btn");
  pageTurnBtn.forEach((el, index) => {
    el.onclick = () => {
      const pageTurnId = el.getAttribute("data-page");
      const pageTurn = document.getElementById(pageTurnId);
      if (pageTurn.classList.contains("turn")) {
        pageTurn.classList.remove("turn");
        setTimeout(() => {
          pageTurn.style.zIndex = 20 - index;
        }, 500);
      } else {
        pageTurn.classList.add("turn");
        setTimeout(() => {
          pageTurn.style.zIndex = 20 + index;
        }, 500);
      }
    };
  });
  
  //contact me button when click
  const pages = document.querySelectorAll(".book-page.page-right");
  const contactMeBtn = document.querySelector(".btn.contact-me");
  contactMeBtn.onclick = () => {
    pages.forEach((page, index) => {
      setTimeout(() => {
        page.classList.add("turn");
        setTimeout(() => {
          page.style.zIndex = 20 + index;
        }, 500);
      }, (index + 1) * 200 + 100);
    });
  };
  
  //create reverse index function
  let totalPages = pages.length;
  let pageNumber = 0;
  function reverseIndex() {
    pageNumber--;
    if (pageNumber < 0) {
      pageNumber = totalPages - 1;
    }
  }
  
  //back profile button when click
  const backProfileBtn = document.querySelector(".back-profile");
  backProfileBtn.onclick = () => {
    pages.forEach((_, index) => {
      setTimeout(() => {
        reverseIndex();
        pages[pageNumber].classList.remove("turn");
  
        setTimeout(() => {
          reverseIndex();
          pages[pageNumber].style.zIndex = 10 + index;
        }, 500);
      }, (index + 1) * 200 + 100);
    });
  };
  
  //opening animation
  const coverRight = document.querySelector(".cover.cover-right");
  const pageLeft = document.querySelector(".book-page.page-left");
  
  //opening animation (cover right animation)
  setTimeout(() => {
    coverRight.classList.add("turn");
  }, 2100);
  setTimeout(() => {
    coverRight.style.zIndex = -1;
  }, 2800);
  
  //opening animation (page left or profile page animation)
  setTimeout(() => {
    pageLeft.style.zIndex = 20;
  }, 3200);
  
  //opening animation (all page right animation)
  pages.forEach((_, index) => {
    setTimeout(() => {
      reverseIndex();
      pages[pageNumber].classList.remove("turn");
      setTimeout(() => {
        reverseIndex();
        pages[pageNumber].style.zIndex = 10 + index;
      }, 500);
    }, (index + 1) * 200 + 2100);
  });
      </script>
    </body>
  </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

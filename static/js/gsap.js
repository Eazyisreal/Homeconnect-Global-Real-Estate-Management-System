        // Create GSAP timeline
        const tl = gsap.timeline({ defaults: { ease: "power1.out", duration: 1.5 } });

        // Animate the video overlay
        tl.to('.video-overlay', { opacity: 0.5, duration: 1 }, 0);

        // Animate the heading and paragraph
        tl.from('.hero h1', { opacity: 0, y: -30 }, "-=1.2")
          .from('.hero p', { opacity: 0, y: 30 }, "-=1");

        // Animate the search form with a slight delay
        tl.from('.advanced-search', { opacity: 0, y: 50, duration: 1.5 }, "-=0.5");

        // Optional: Animate the search button separately for more staggered effect
        tl.from('.advanced-search-btn-container', { opacity: 0, y: 50, duration: 1 }, "-=1.5");

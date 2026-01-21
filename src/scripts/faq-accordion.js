// FAQ Accordion Functionality
document.addEventListener('DOMContentLoaded', function() {
    // FAQ 349 - Side By Side
    const faqItems349 = document.querySelectorAll('#faq-349 .cs-faq-item');
    faqItems349.forEach(item => {
        const button = item.querySelector('.cs-button');
        const content = item.querySelector('.cs-item-p');
        
        if (button && content) {
            button.addEventListener('click', () => {
                // Close all other items
                faqItems349.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current item
                item.classList.toggle('active');
            });
        }
    });
    
    // FAQ 351 - Standard
    const faqItems351 = document.querySelectorAll('#faq-351 .cs-faq-item');
    faqItems351.forEach(item => {
        const button = item.querySelector('.cs-button');
        const content = item.querySelector('.cs-item-p');
        
        if (button && content) {
            button.addEventListener('click', () => {
                // Close all other items
                faqItems351.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current item
                item.classList.toggle('active');
            });
        }
    });
});
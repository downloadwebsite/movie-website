/**
 * Movie Download Website - Main JavaScript
 */

$(document).ready(function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scroll for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 500);
        }
    });

    // Add to favorites (AJAX)
    $('.favorite-btn').on('click', function(e) {
        e.preventDefault();
        var btn = $(this);
        var url = btn.data('url');

        $.ajax({
            url: url,
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.status === 'added') {
                    btn.find('.favorite-text').text('حذف از علاقه‌مندی');
                    btn.addClass('btn-danger').removeClass('btn-outline-danger');
                    showToast('به علاقه‌مندی‌ها اضافه شد', 'success');
                } else {
                    btn.find('.favorite-text').text('افزودن به علاقه‌مندی');
                    btn.addClass('btn-outline-danger').removeClass('btn-danger');
                    showToast('از علاقه‌مندی‌ها حذف شد', 'info');
                }
            },
            error: function() {
                showToast('خطا در انجام عملیات', 'error');
            }
        });
    });

    // Reply buttons
    $('.reply-btn').on('click', function() {
        var commentId = $(this).data('comment-id');
        $('#reply-form-' + commentId).removeClass('d-none');
        $('#reply-form-' + commentId).find('textarea').focus();
    });

    $('.cancel-reply').on('click', function() {
        $(this).closest('.reply-form').addClass('d-none');
    });

    // Rating stars hover effect
    $('.rating-star').on('mouseenter', function() {
        var score = $(this).data('score');
        $('.rating-stars .rating-star').each(function(index) {
            if (index < score) {
                $(this).find('i').css('color', '#ffc107');
            } else {
                $(this).find('i').css('color', '#ccc');
            }
        });
    });

    $('.rating-stars').on('mouseleave', function() {
        $('.rating-stars .rating-star').each(function() {
            if ($(this).find('i').hasClass('active')) {
                $(this).find('i').css('color', '#ffc107');
            } else {
                $(this).find('i').css('color', '#ccc');
            }
        });
    });

    // Search input focus
    $('input[name="q"]').on('focus', function() {
        $(this).closest('.input-group').addClass('shadow');
    });

    $('input[name="q"]').on('blur', function() {
        $(this).closest('.input-group').removeClass('shadow');
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        var imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(function(img) {
            imageObserver.observe(img);
        });
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toast notification function
function showToast(message, type) {
    var toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.cssText = 'position: fixed; top: 20px; left: 20px; z-index: 9999;';
        document.body.appendChild(toastContainer);
    }

    var toast = document.createElement('div');
    var bgColor = type === 'success' ? '#198754' : type === 'error' ? '#dc3545' : '#0dcaf0';
    toast.style.cssText = 'background: ' + bgColor + '; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); animation: slideIn 0.3s ease;';
    toast.textContent = message;
    toastContainer.appendChild(toast);

    setTimeout(function() {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations for toast
var style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(-100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

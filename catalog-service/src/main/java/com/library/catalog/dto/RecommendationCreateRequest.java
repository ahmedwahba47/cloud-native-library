package com.library.catalog.dto;

import jakarta.validation.constraints.*;

public class RecommendationCreateRequest {

    @NotNull(message = "Book ID is required")
    private Long bookId;

    @NotBlank(message = "Recommender name is required")
    private String recommendedBy;

    private String reason;

    @NotNull(message = "Rating is required")
    @Min(value = 1, message = "Rating must be between 1 and 5")
    @Max(value = 5, message = "Rating must be between 1 and 5")
    private Integer rating;

    public RecommendationCreateRequest() {}

    public RecommendationCreateRequest(Long bookId, String recommendedBy, String reason, Integer rating) {
        this.bookId = bookId;
        this.recommendedBy = recommendedBy;
        this.reason = reason;
        this.rating = rating;
    }

    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
    public String getRecommendedBy() { return recommendedBy; }
    public void setRecommendedBy(String recommendedBy) { this.recommendedBy = recommendedBy; }
    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }
    public Integer getRating() { return rating; }
    public void setRating(Integer rating) { this.rating = rating; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Long bookId;
        private String recommendedBy;
        private String reason;
        private Integer rating;

        public Builder bookId(Long bookId) { this.bookId = bookId; return this; }
        public Builder recommendedBy(String recommendedBy) { this.recommendedBy = recommendedBy; return this; }
        public Builder reason(String reason) { this.reason = reason; return this; }
        public Builder rating(Integer rating) { this.rating = rating; return this; }
        public RecommendationCreateRequest build() { return new RecommendationCreateRequest(bookId, recommendedBy, reason, rating); }
    }
}

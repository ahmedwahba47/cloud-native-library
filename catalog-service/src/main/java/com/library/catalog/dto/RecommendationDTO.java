package com.library.catalog.dto;

import java.time.LocalDate;

public class RecommendationDTO {
    private Long id;
    private Long bookId;
    private String bookTitle;
    private String bookAuthor;
    private String recommendedBy;
    private String reason;
    private Integer rating;
    private LocalDate createdDate;

    public RecommendationDTO() {}

    public RecommendationDTO(Long id, Long bookId, String bookTitle, String bookAuthor, String recommendedBy, String reason, Integer rating, LocalDate createdDate) {
        this.id = id;
        this.bookId = bookId;
        this.bookTitle = bookTitle;
        this.bookAuthor = bookAuthor;
        this.recommendedBy = recommendedBy;
        this.reason = reason;
        this.rating = rating;
        this.createdDate = createdDate;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
    public String getBookTitle() { return bookTitle; }
    public void setBookTitle(String bookTitle) { this.bookTitle = bookTitle; }
    public String getBookAuthor() { return bookAuthor; }
    public void setBookAuthor(String bookAuthor) { this.bookAuthor = bookAuthor; }
    public String getRecommendedBy() { return recommendedBy; }
    public void setRecommendedBy(String recommendedBy) { this.recommendedBy = recommendedBy; }
    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }
    public Integer getRating() { return rating; }
    public void setRating(Integer rating) { this.rating = rating; }
    public LocalDate getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDate createdDate) { this.createdDate = createdDate; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Long id;
        private Long bookId;
        private String bookTitle;
        private String bookAuthor;
        private String recommendedBy;
        private String reason;
        private Integer rating;
        private LocalDate createdDate;

        public Builder id(Long id) { this.id = id; return this; }
        public Builder bookId(Long bookId) { this.bookId = bookId; return this; }
        public Builder bookTitle(String bookTitle) { this.bookTitle = bookTitle; return this; }
        public Builder bookAuthor(String bookAuthor) { this.bookAuthor = bookAuthor; return this; }
        public Builder recommendedBy(String recommendedBy) { this.recommendedBy = recommendedBy; return this; }
        public Builder reason(String reason) { this.reason = reason; return this; }
        public Builder rating(Integer rating) { this.rating = rating; return this; }
        public Builder createdDate(LocalDate createdDate) { this.createdDate = createdDate; return this; }
        public RecommendationDTO build() { return new RecommendationDTO(id, bookId, bookTitle, bookAuthor, recommendedBy, reason, rating, createdDate); }
    }
}

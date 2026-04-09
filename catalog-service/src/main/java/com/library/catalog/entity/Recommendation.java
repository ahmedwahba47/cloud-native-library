package com.library.catalog.entity;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "recommendations")
public class Recommendation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "book_id", nullable = false)
    private Long bookId;

    @Column(name = "recommended_by", nullable = false)
    private String recommendedBy;

    @Column(length = 500)
    private String reason;

    @Column(nullable = false)
    private Integer rating;

    @Column(name = "created_date")
    private LocalDate createdDate;

    public Recommendation() {}

    public Recommendation(Long id, Long bookId, String recommendedBy, String reason, Integer rating, LocalDate createdDate) {
        this.id = id;
        this.bookId = bookId;
        this.recommendedBy = recommendedBy;
        this.reason = reason;
        this.rating = rating;
        this.createdDate = createdDate;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
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
        private String recommendedBy;
        private String reason;
        private Integer rating;
        private LocalDate createdDate;

        public Builder id(Long id) { this.id = id; return this; }
        public Builder bookId(Long bookId) { this.bookId = bookId; return this; }
        public Builder recommendedBy(String recommendedBy) { this.recommendedBy = recommendedBy; return this; }
        public Builder reason(String reason) { this.reason = reason; return this; }
        public Builder rating(Integer rating) { this.rating = rating; return this; }
        public Builder createdDate(LocalDate createdDate) { this.createdDate = createdDate; return this; }
        public Recommendation build() { return new Recommendation(id, bookId, recommendedBy, reason, rating, createdDate); }
    }
}

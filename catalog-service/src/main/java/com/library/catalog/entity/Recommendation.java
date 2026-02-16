package com.library.catalog.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Entity
@Table(name = "recommendations")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
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
}

package com.library.catalog.repository;

import com.library.catalog.entity.Recommendation;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RecommendationRepository extends JpaRepository<Recommendation, Long> {
    Page<Recommendation> findByBookId(Long bookId, Pageable pageable);
}

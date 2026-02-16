package com.library.catalog.repository;

import com.library.catalog.entity.ReadingListItem;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ReadingListItemRepository extends JpaRepository<ReadingListItem, Long> {
}

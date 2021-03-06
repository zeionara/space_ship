package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.GenBoatCapacityAndQuantityForRequirementContent;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;

public class boats {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenName
    private String name;
    @GenBoatCapacityAndQuantityForRequirementContent
    private Integer capacity;
}

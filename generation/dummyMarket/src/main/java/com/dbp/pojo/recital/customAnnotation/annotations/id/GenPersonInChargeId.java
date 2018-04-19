package com.dbp.pojo.recital.customAnnotation.annotations.id;

import com.dbp.pojo.recital.customAnnotation.impl.id.PersonInChargeIdGenerator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(PersonInChargeIdGenerator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenPersonInChargeId {
}


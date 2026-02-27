package org.example.utils;

import java.lang.reflect.Method;
import java.lang.reflect.Field;

/**
 * ReflectionUtils: Utility class for reflection operations
 * Used for dynamic method and field access in page objects
 */
public class ReflectionUtils {

    /**
     * Get all methods from a class
     */
    public static Method[] getAllMethods(Class<?> clazz) {
        return clazz.getDeclaredMethods();
    }

    /**
     * Get all fields from a class
     */
    public static Field[] getAllFields(Class<?> clazz) {
        return clazz.getDeclaredFields();
    }

    /**
     * Invoke a method using reflection
     */
    public static Object invokeMethod(Object obj, String methodName, Class<?>[] parameterTypes, Object[] parameters) {
        try {
            Method method = obj.getClass().getDeclaredMethod(methodName, parameterTypes);
            method.setAccessible(true);
            return method.invoke(obj, parameters);
        } catch (Exception e) {
            throw new RuntimeException("Failed to invoke method: " + methodName, e);
        }
    }

    /**
     * Get field value using reflection
     */
    public static Object getFieldValue(Object obj, String fieldName) {
        try {
            Field field = obj.getClass().getDeclaredField(fieldName);
            field.setAccessible(true);
            return field.get(obj);
        } catch (Exception e) {
            throw new RuntimeException("Failed to get field value: " + fieldName, e);
        }
    }

    /**
     * Set field value using reflection
     */
    public static void setFieldValue(Object obj, String fieldName, Object value) {
        try {
            Field field = obj.getClass().getDeclaredField(fieldName);
            field.setAccessible(true);
            field.set(obj, value);
        } catch (Exception e) {
            throw new RuntimeException("Failed to set field value: " + fieldName, e);
        }
    }

    /**
     * Check if method exists in class
     */
    public static boolean methodExists(Class<?> clazz, String methodName, Class<?>[] parameterTypes) {
        try {
            clazz.getDeclaredMethod(methodName, parameterTypes);
            return true;
        } catch (NoSuchMethodException e) {
            return false;
        }
    }

    /**
     * Check if field exists in class
     */
    public static boolean fieldExists(Class<?> clazz, String fieldName) {
        try {
            clazz.getDeclaredField(fieldName);
            return true;
        } catch (NoSuchFieldException e) {
            return false;
        }
    }

    /**
     * Get all methods annotated with a specific annotation
     */
    public static Method[] getMethodsWithAnnotation(Class<?> clazz, Class<?> annotationClass) {
        return java.util.Arrays.stream(getAllMethods(clazz))
                .filter(method -> method.isAnnotationPresent((Class<java.lang.annotation.Annotation>) annotationClass))
                .toArray(Method[]::new);
    }
}


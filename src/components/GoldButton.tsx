import React from 'react';
import { StyleSheet, TouchableOpacity, Text, ActivityIndicator, ViewStyle } from 'react-native';
import { Colors, Radius, Typography, Spacing } from '../theme';

interface GoldButtonProps {
  label: string;
  onPress: () => void;
  loading?: boolean;
  disabled?: boolean;
  variant?: 'filled' | 'outlined' | 'text';
  style?: ViewStyle;
  fullWidth?: boolean;
}

export function GoldButton({
  label, onPress, loading = false, disabled = false,
  variant = 'filled', style, fullWidth = false,
}: GoldButtonProps) {
  const isDisabled = disabled || loading;

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={isDisabled}
      activeOpacity={0.75}
      style={[
        styles.base,
        variant === 'filled'   && styles.filled,
        variant === 'outlined' && styles.outlined,
        variant === 'text'     && styles.text,
        isDisabled             && styles.disabled,
        fullWidth              && styles.fullWidth,
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator
          color={variant === 'filled' ? Colors.onPrimary : Colors.primary}
          size="small"
        />
      ) : (
        <Text
          style={[
            styles.label,
            variant === 'filled'   && styles.labelFilled,
            variant === 'outlined' && styles.labelOutlined,
            variant === 'text'     && styles.labelText,
            isDisabled             && styles.labelDisabled,
          ]}
        >
          {label}
        </Text>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  base: {
    paddingVertical: Spacing.sm + 4,
    paddingHorizontal: Spacing.lg,
    borderRadius: Radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: 120,
  },
  filled: {
    backgroundColor: Colors.primary,
  },
  outlined: {
    borderWidth: 1.5,
    borderColor: Colors.primary,
    backgroundColor: 'transparent',
  },
  text: {
    backgroundColor: 'transparent',
  },
  disabled: {
    opacity: 0.45,
  },
  fullWidth: {
    width: '100%',
  },
  label: {
    fontSize: 15,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  labelFilled: {
    color: Colors.onPrimary,
  },
  labelOutlined: {
    color: Colors.primary,
  },
  labelText: {
    color: Colors.primary,
  },
  labelDisabled: {
    opacity: 0.6,
  },
});
